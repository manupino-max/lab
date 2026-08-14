import json
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.kernel_approximation import Nystroem
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEEDS=list(range(20))
DOSES=np.round(np.linspace(0,1.25,26),4)
MASSES=np.round(np.linspace(0,1.0,21),4)
EPS=0.02


def auc_oriented(y,p):
    a=roc_auc_score(y,p)
    return max(a,1-a)


def split(n,seed):
    rng=np.random.default_rng(seed); idx=rng.permutation(n); cut=int(.7*n); return idx[:cut],idx[cut:]


def one(seed,mu_scale=1.0,cov_ratio=1.0):
    rng=np.random.default_rng(seed); n0=n1=1200; d=32
    mu0=np.zeros(d); direction=rng.normal(size=d); direction/=np.linalg.norm(direction); mu1=mu_scale*2.0*direction
    S=np.eye(d)
    # matched covariance control; optional anisotropic nuisance kept identical across groups
    A=rng.normal(size=(d,d))/np.sqrt(d); S=A@A.T + 0.5*np.eye(d)
    X0=rng.multivariate_normal(mu0,S,n0); X1=rng.multivariate_normal(mu1,S*cov_ratio,n1)
    X=np.vstack([X0,X1]); G=np.r_[np.zeros(n0,int),np.ones(n1,int)]
    tr,te=split(len(G),seed)
    rows=[]
    for dose in DOSES:
        Xd=X.copy(); Xd[G==1] -= dose*(mu1-mu0)
        clf=LogisticRegression(max_iter=4000).fit(Xd[tr],G[tr]); p=clf.predict_proba(Xd[te])[:,1]
        al=auc_oriented(G[te],p)
        # RBF probe to distinguish remaining nonlinear/distributional signal
        rbf=make_pipeline(StandardScaler(),Nystroem(kernel='rbf',gamma='scale',n_components=160,random_state=seed),LogisticRegression(max_iter=3000))
        rbf.fit(Xd[tr],G[tr]); pr=rbf.predict_proba(Xd[te])[:,1]; ar=auc_oriented(G[te],pr)
        rows.append({'seed':seed,'experiment':'dose','dose':float(dose),'linear_auc':float(al),'rbf_auc':float(ar),'residual_mean_norm':float(np.linalg.norm((1-dose)*(mu1-mu0)))})
    # partial mass: move only a fraction of G=1 points the full delta_mu
    for mass in MASSES:
        Xd=X.copy(); idx=np.flatnonzero(G==1); k=int(round(mass*len(idx))); pick=rng.choice(idx,size=k,replace=False); Xd[pick]-=(mu1-mu0)
        clf=LogisticRegression(max_iter=4000).fit(Xd[tr],G[tr]); p=clf.predict_proba(Xd[te])[:,1]
        al=auc_oriented(G[te],p)
        rbf=make_pipeline(StandardScaler(),Nystroem(kernel='rbf',gamma='scale',n_components=160,random_state=seed),LogisticRegression(max_iter=3000))
        rbf.fit(Xd[tr],G[tr]); pr=rbf.predict_proba(Xd[te])[:,1]; ar=auc_oriented(G[te],pr)
        rows.append({'seed':seed,'experiment':'mass','mass':float(mass),'linear_auc':float(al),'rbf_auc':float(ar),'residual_mean_norm':float(np.linalg.norm((1-mass)*(mu1-mu0)))})
    return rows

allrows=[]
for cov_ratio in (1.0,1.5):
    for seed in SEEDS:
        rs=one(seed,mu_scale=1.0,cov_ratio=cov_ratio)
        for r in rs:r['cov_ratio']=cov_ratio
        allrows.extend(rs)

out=Path('results/m2_critical_mass_deltamu'); out.mkdir(parents=True,exist_ok=True)
import csv
with (out/'results.csv').open('w',newline='') as f:
    fields=sorted({k for r in allrows for k in r}); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(allrows)

summary={}
for exp,key in [('dose','dose'),('mass','mass')]:
    sub=[r for r in allrows if r['experiment']==exp and r['cov_ratio']==1.0]
    by={}
    for r in sub: by.setdefault(round(r[key],4),[]).append(r['linear_auc'])
    means={k:float(np.mean(v)) for k,v in by.items()}
    critical=next((k for k,v in means.items() if v<=0.5+EPS),None)
    summary[exp]={'critical':critical,'threshold_eps':EPS,'means_linear_auc':means}
(out/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({'status':'PASS','rows':len(allrows),'summary':summary}))
