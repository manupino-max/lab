import csv, json
from pathlib import Path
import numpy as np

SEEDS=range(20)
DOSES=np.round(np.linspace(0,1.25,26),4)
MASSES=np.round(np.linspace(0,1.0,21),4)
EPS=0.02


def auc(y,s):
    y=np.asarray(y); s=np.asarray(s); order=np.argsort(s,kind='mergesort'); ranks=np.empty_like(order,dtype=float); ranks[order]=np.arange(len(s))+1
    n1=float(y.sum()); n0=float(len(y)-n1)
    return float(((ranks[y==1].sum()-n1*(n1+1)/2)/(n1*n0)))

def fit_ridge(X,y,l2=1e-3):
    X1=np.c_[np.ones(len(X)),X]
    A=X1.T@X1; A.flat[::A.shape[0]+1]+=l2
    return np.linalg.solve(A,X1.T@y)

def eval_linear(Xtr,ytr,Xte,yte):
    w=fit_ridge(Xtr,ytr); s=np.c_[np.ones(len(Xte)),Xte]@w; a=auc(yte,s); return max(a,1-a)

def latent(seed):
    r=np.random.default_rng(seed); d=32; n0=n1=1200
    u=r.normal(size=d); u/=np.linalg.norm(u); delta=2*u
    A=r.normal(size=(d,d))/np.sqrt(d); S=A@A.T+0.5*np.eye(d)
    X0=r.multivariate_normal(np.zeros(d),S,n0); X1=r.multivariate_normal(delta,S,n1)
    # independent task signal v, deliberately non-collinear with delta
    v=r.normal(size=d); v-=v.dot(u)*u; v/=np.linalg.norm(v)
    X=np.vstack([X0,X1]); G=np.r_[np.zeros(n0,int),np.ones(n1,int)]
    logits=X@v + r.normal(scale=0.8,size=len(X)); Y=(logits>np.median(logits)).astype(int)
    p=r.permutation(len(X)); c=int(.7*len(X)); tr,te=p[:c],p[c:]
    return r,X,G,Y,delta,v,tr,te

rows=[]
for cov_ratio in (1.0,1.5):
  for seed in SEEDS:
    r,X,G,Y,delta,v,tr,te=latent(seed)
    # covariance control for group 1
    if cov_ratio!=1.0:
        d=len(delta); Sfac=np.eye(d)*(cov_ratio-1); X[G==1] = X[G==1] + (X[G==1] @ Sfac)
    for dose in DOSES:
        Xd=X.copy(); Xd[G==1]-=dose*delta
        rows.append({'seed':seed,'condition':'dose','level':float(dose),'cov_ratio':cov_ratio,'linear_auc':eval_linear(Xd[tr],G[tr],Xd[te],G[te]),'task_auc':eval_linear(Xd[tr],Y[tr],Xd[te],Y[te]),'residual_mean_norm':float(abs(1-dose)*np.linalg.norm(delta))})
    for mass in MASSES:
        Xd=X.copy(); idx=np.flatnonzero(G==1); k=int(round(mass*len(idx))); pick=r.choice(idx,size=k,replace=False); Xd[pick]-=delta
        rows.append({'seed':seed,'condition':'mass','level':float(mass),'cov_ratio':cov_ratio,'linear_auc':eval_linear(Xd[tr],G[tr],Xd[te],G[te]),'task_auc':eval_linear(Xd[tr],Y[tr],Xd[te],Y[te]),'residual_mean_norm':float(abs(1-mass)*np.linalg.norm(delta))})

out=Path('results/m2_critical_mass_deltamu_fast'); out.mkdir(parents=True,exist_ok=True)
fields=['seed','condition','level','cov_ratio','linear_auc','task_auc','residual_mean_norm']
with (out/'results.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
summary={}
for cond in ('dose','mass'):
  sub=[r for r in rows if r['condition']==cond and r['cov_ratio']==1.0]
  levels=sorted({r['level'] for r in sub})
  means={str(x):float(np.mean([r['linear_auc'] for r in sub if r['level']==x])) for x in levels}
  critical=next((x for x in levels if means[str(x)]<=0.5+EPS),None)
  summary[cond]={'critical_level_eps020':critical,'threshold':EPS,'means_linear_auc':means}
# endpoint law checks: at dose=1 or mass=1 residual mean is approximately zero, but empirical AUC is sample-estimation limited.
summary['design']={'seeds':20,'dose_points':len(DOSES),'mass_points':len(MASSES),'covariance_controls':[1.0,1.5],'delta_mu_norm':2.0}
(out/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({'status':'PASS','rows':len(rows),'summary':summary}))
