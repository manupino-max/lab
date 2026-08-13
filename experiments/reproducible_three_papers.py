# temporary syntax-safe replacement
from pathlib import Path
import csv, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

OUT=Path("results/three_papers"); OUT.mkdir(parents=True, exist_ok=True)

def p01(seed):
    rng=np.random.default_rng(seed); rows=[]
    for inj in ["translation","rotation","anisotropic_scale","shear","local_warp","radial_warp","twist","noise","compression","expansion","mixed"]:
        for a in [0,.25,.5,.75]:
            z=rng.normal(size=(150,8)); z[:,0]+= (inj in ["translation","mixed"])*a
            if inj=="rotation":
                q=z[:,0].copy(); z[:,0]=np.cos(a)*q-np.sin(a)*z[:,1]; z[:,1]=np.sin(a)*q+np.cos(a)*z[:,1]
            elif inj=="anisotropic_scale": z[:,0]*=1+2*a
            elif inj=="shear": z[:,0]+=a*z[:,1]
            elif inj in ["local_warp","radial_warp"]: z[:,0]+=a*np.tanh(z[:,1])*.8
            elif inj=="twist":
                t=a*z[:,2]; x,y=z[:,0].copy(),z[:,1].copy(); z[:,0]=np.cos(t)*x-np.sin(t)*y; z[:,1]=np.sin(t)*x+np.cos(t)*y
            elif inj=="noise": z+=rng.normal(0,a*.5,z.shape)
            elif inj=="compression": z[:,0]/=1+a
            elif inj=="expansion": z[:,0]*=1+a
            elif inj=="mixed": z[:,0]+=a*z[:,1]; z[:,2]*=1+a
            rows.append(dict(seed=seed,injector=inj,alpha=a,Dc=float(np.mean(np.linalg.norm(z-z.mean(0),axis=1))),Dg=float(np.linalg.norm(z.mean(0))),Ds=float(np.std(np.linalg.norm(z,axis=1)))))
    return rows

def leace(X,s):
    xc=X-X.mean(0); sc=s.reshape(-1,1)-s.reshape(-1,1).mean(0); v=np.linalg.lstsq(sc,xc,rcond=None)[0].T
    denom=float((v.T@v).item())+1e-12
    return xc@(np.eye(X.shape[1])-v@v.T/denom)

def p02(seed):
    rng=np.random.default_rng(seed); n=800; d=12; s=rng.integers(0,2,n); X=rng.normal(size=(n,d)); X[:,0]+=.9*s; X[:,1]+=1.8*(s-.5)**2+.8*(s-.5)*np.abs(X[:,2]); y=(X[:,3]+.8*s+rng.normal(size=n)>0).astype(int)
    Xtr,Xte,str_,ste,ytr,yte=train_test_split(X,s,y,test_size=.35,random_state=seed,stratify=s); Ztr=leace(Xtr,str_); Zte=leace(Xte,ste)
    lin=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000)).fit(Ztr,str_); rbf=make_pipeline(StandardScaler(),SVC(kernel="rbf",probability=True)).fit(Ztr,str_); task=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000)).fit(Ztr,ytr)
    return dict(seed=seed,linear_auc=roc_auc_score(ste,lin.predict_proba(Zte)[:,1]),nonlinear_auc=roc_auc_score(ste,rbf.predict_proba(Zte)[:,1]),utility_auc=roc_auc_score(yte,task.predict_proba(Zte)[:,1]))

def p03(seed):
    rng=np.random.default_rng(seed); n=1200; d=10; s=rng.integers(0,2,n); X=rng.normal(size=(n,d)); X[:,0]+=1.8*s; y=(X[:,1]+.7*s+rng.normal(size=n)>.5).astype(int); tr,te=train_test_split(np.arange(n),test_size=.35,random_state=seed,stratify=s); rows=[]
    for lam in np.linspace(0,1,6):
        Z=X.copy(); gm=np.vstack([Z[s==g].mean(0) for g in [0,1]]); Z=(1-lam)*Z+lam*(Z-np.array([gm[g] for g in s])); clf=LogisticRegression(max_iter=2000).fit(Z[tr],y[tr]); pred=(clf.predict_proba(Z[te])[:,1]>=.5).astype(int); st=s[te]; yt=y[te]
        tpr1=((pred[st==1]==1)&(yt[st==1]==1)).sum()/max((yt[st==1]==1).sum(),1); tpr0=((pred[st==0]==1)&(yt[st==0]==1)).sum()/max((yt[st==0]==1).sum(),1)
        rows.append(dict(seed=seed,lambda_=float(lam),distortion=float(np.mean(np.linalg.norm(Z[te]-X[te],axis=1))),DP_gap=float(abs(pred[st==1].mean()-pred[st==0].mean())),EO_gap=float(abs(tpr1-tpr0)),accuracy=float(accuracy_score(yt,pred))))
    return rows

def main():
    allrows=[]
    for seed in [11,22,33,44,55]: allrows += [dict(experiment="P01_GMRB",**r) for r in p01(seed)]+[dict(experiment="P02_LEACE",**p02(seed))]+[dict(experiment="P03_FRONTIER",**r) for r in p03(seed)]
    with (OUT/"results.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=sorted({k for r in allrows for k in r})); w.writeheader(); w.writerows(allrows)
    p01r=[r for r in allrows if r["experiment"]=="P01_GMRB" and r["alpha"]>.0]; p02r=[r for r in allrows if r["experiment"]=="P02_LEACE"]; p03r=[r for r in allrows if r["experiment"]=="P03_FRONTIER"]; denom=sum(r["alpha"]==.25 for r in p01r); leaders=sum(r["Dc"]<=min(r["Dg"],r["Ds"]) for r in p01r if r["alpha"]==.25)
    summary={"P01":{"alpha_025_Dc_leadership":leaders/max(denom,1),"n_trajectories":denom},"P02":{"mean_linear_auc":float(np.mean([r["linear_auc"] for r in p02r])),"mean_nonlinear_auc":float(np.mean([r["nonlinear_auc"] for r in p02r])),"mean_utility_auc":float(np.mean([r["utility_auc"] for r in p02r]))},"P03":{"best_accuracy":float(max(r["accuracy"] for r in p03r)),"min_DP_gap":float(min(r["DP_gap"] for r in p03r)),"min_EO_gap":float(min(r["EO_gap"] for r in p03r)),"n_rows":len(p03r)}}
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n"); print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
