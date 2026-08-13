"""Clean-room reproducibility suite for the three current paper candidates.

No private repository files, historical result files, or datasets are read.
All inputs are generated at runtime. The three experiments are deliberately
self-contained so that a public GitHub Actions run can reproduce the checks.
"""
from pathlib import Path
import csv, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

OUT=Path("results/three_papers")
OUT.mkdir(parents=True,exist_ok=True)

# ---------------- P01 GMR-B: controlled geometric perturbations ----------------
def p01(seed):
    rng=np.random.default_rng(seed); rows=[]
    injectors=["translation","rotation","anisotropic_scale","shear","local_warp","radial_warp","twist","noise","compression","expansion","mixed"]
    alphas=[0,.25,.5,.75]
    for inj in injectors:
        for a in alphas:
            z=rng.normal(size=(150,8)); z[:,0]=z[:,0]+(inj in ["translation","mixed"])*a
            if inj=="rotation":
                q=z[:,0].copy(); z[:,0]=np.cos(a)*q-np.sin(a)*z[:,1]; z[:,1]=np.sin(a)*q+np.cos(a)*z[:,1]
            elif inj=="anisotropic_scale": z[:,0]*=1+2*a
            elif inj=="shear": z[:,0]+=a*z[:,1]
            elif inj in ["local_warp","radial_warp"]: z[:,0]+=a*np.tanh(z[:,1])*0.8
            elif inj=="twist":
                t=a*z[:,2]; x,y=z[:,0].copy(),z[:,1].copy(); z[:,0]=np.cos(t)*x-np.sin(t)*y; z[:,1]=np.sin(t)*x+np.cos(t)*y
            elif inj=="noise": z+=rng.normal(0,a*.5,z.shape)
            elif inj=="compression": z[:,0]/=1+a
            elif inj=="expansion": z[:,0]*=1+a
            elif inj=="mixed": z[:,0]+=a*z[:,1]; z[:,2]*=1+a
            # Dc: distance from centroid after removing translation; Dg: global displacement.
            dc=float(np.mean(np.linalg.norm(z-z.mean(0),axis=1)))
            dg=float(np.linalg.norm(z.mean(0)))
            ds=float(np.std(np.linalg.norm(z,axis=1)))
            rows.append(dict(seed=seed,injector=inj,alpha=a,Dc=dc,Dg=dg,Ds=ds))
    return rows

# ---------------- P02 LEACE vs nonlinear residual ----------------
def leace(X,s):
    # Orthogonal projection removing the least-squares linear concept direction.
    s=s.reshape(-1,1); xc=X-X.mean(0); sc=s-s.mean(0)
    w=np.linalg.lstsq(sc,xc,rcond=None)[0]  # 1 x d
    v=w.T; denom=float(v.T@v)+1e-12
    P=np.eye(X.shape[1])-v@v.T/denom
    return xc@P

def p02(seed):
    rng=np.random.default_rng(seed); n=800; d=12
    s=rng.integers(0,2,n)
    # Nonlinear group signal survives linear erasure through a quadratic coordinate.
    X=rng.normal(0,1,(n,d)); X[:,0]+=0.9*s; X[:,1]+=1.8*(s-.5)**2 + 0.8*(s-.5)*np.abs(X[:,2])
    y=(X[:,3]+0.8*s+rng.normal(size=n)>0).astype(int)
    Xtr,Xte,str_,ste,ytr,yte=train_test_split(X,s,y,test_size=.35,random_state=seed,stratify=s)
    Ztr=leace(Xtr,str_); Zte=leace(Xte,ste)
    lin=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000)).fit(Ztr,str_)
    rbf=make_pipeline(StandardScaler(),SVC(kernel="rbf",probability=True)).fit(Ztr,str_)
    task=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000)).fit(Ztr,ytr)
    return dict(seed=seed,linear_auc=roc_auc_score(ste,lin.predict_proba(Zte)[:,1]),nonlinear_auc=roc_auc_score(ste,rbf.predict_proba(Zte)[:,1]),utility_auc=roc_auc_score(yte,task.predict_proba(Zte)[:,1]))

# ---------------- P03 structural fairness frontier ----------------
def p03(seed):
    rng=np.random.default_rng(seed); n=1200; d=10
    s=rng.integers(0,2,n); X=rng.normal(size=(n,d)); X[:,0]+=1.8*s; y=(X[:,1]+.7*s+rng.normal(size=n)>.5).astype(int)
    tr,te=train_test_split(np.arange(n),test_size=.35,random_state=seed,stratify=s)
    rows=[]
    for lam in np.linspace(0,1,6):
        # Controlled representation suppression: interpolate toward group-centred representation.
        Z=X.copy(); group_mean=np.vstack([Z[s==g].mean(0) for g in [0,1]])
        Z=(1-lam)*Z + lam*(Z-np.array([group_mean[g] for g in s]))
        clf=LogisticRegression(max_iter=2000).fit(Z[tr],y[tr]); p=clf.predict_proba(Z[te])[:,1]; pred=(p>=.5).astype(int)
        dp=abs(pred[s[te]==1].mean()-pred[s[te]==0].mean())
        tpr1=((pred[s[te]==1]==1)&(y[te]==1)).sum()/max((y[te][s[te]==1]==1).sum(),1)
        tpr0=((pred[s[te]==0]==1)&(y[te]==0)==False).sum() if False else ((pred[s[te]==0]==1)&(y[te]==1)).sum()/max((y[te][s[te]==0]==1).sum(),1)
        eo=abs(tpr1-tpr0)
        acc=accuracy_score(y[te],pred)
        distortion=float(np.mean(np.linalg.norm(Z[te]-X[te],axis=1)))
        rows.append(dict(seed=seed,lambda_=float(lam),distortion=distortion,DP_gap=dp,EO_gap=eo,accuracy=acc))
    return rows

def main():
    allrows=[]
    for seed in [11,22,33,44,55]:
        allrows += [dict(experiment="P01_GMRB",**r) for r in p01(seed)]
        allrows += [dict(experiment="P02_LEACE",**p02(seed))]
        allrows += [dict(experiment="P03_FRONTIER",**r) for r in p03(seed)]
    with (OUT/"results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=sorted({k for r in allrows for k in r})); w.writeheader(); w.writerows(allrows)
    p01r=[r for r in allrows if r["experiment"]=="P01_GMRB" and r["alpha"]>.0]
    # low-alpha leadership among Dc,Dg,Ds
    leaders=sum(r["Dc"]<=min(r["Dg"],r["Ds"]) for r in p01r if r["alpha"]==.25); denom=sum(r["alpha"]==.25 for r in p01r)
    p02r=[r for r in allrows if r["experiment"]=="P02_LEACE"]
    p03r=[r for r in allrows if r["experiment"]=="P03_FRONTIER"]
    summary={"P01":{"alpha_025_Dc_leadership":leaders/max(denom,1),"n_trajectories":denom},"P02":{"mean_linear_auc":float(np.mean([r["linear_auc"] for r in p02r])),"mean_nonlinear_auc":float(np.mean([r["nonlinear_auc"] for r in p02r])),"mean_utility_auc":float(np.mean([r["utility_auc"] for r in p02r]))},"P03":{"best_accuracy":float(max(r["accuracy"] for r in p03r)),"min_DP_gap":float(min(r["DP_gap"] for r in p03r)),"min_EO_gap":float(min(r["EO_gap"] for r in p03r)),"n_rows":len(p03r)}}
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
