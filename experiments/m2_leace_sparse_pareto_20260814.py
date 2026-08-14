"""M2 sparse/localized LEACE Pareto experiment."""
from __future__ import annotations
import csv, json, hashlib
from pathlib import Path
import numpy as np
import torch
from scipy.stats import gaussian_kde, wilcoxon
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, balanced_accuracy_score
from concept_erasure import LeaceEraser

SEEDS=list(range(20)); N=1200; D=32; TEST=.30
KFRACS=[.02,.05,.10,.20,.40,.60,1.00]; LAMBDAS=[.25,.50,.75,1.00]
OUT=Path('results/M2_LEACE_SPARSE_PARETO_20260814'); OUT.mkdir(parents=True,exist_ok=True)

def oa(y,s):
 a=float(roc_auc_score(y,s)); return max(a,1-a)

def mode1d(v):
 v=np.asarray(v,float)
 if np.std(v)<1e-12:return float(np.mean(v))
 kde=gaussian_kde(v); lo,hi=np.quantile(v,[.01,.99]); grid=np.linspace(lo,hi,1024)
 return float(grid[np.argmax(kde(grid))])

def data(seed):
 r=np.random.default_rng(seed); g=np.r_[np.zeros(N//2,int),np.ones(N//2,int)]
 u=r.normal(size=D);u/=np.linalg.norm(u)
 t=r.normal(size=D);t-=t@u*u;t/=np.linalg.norm(t)
 X=r.normal(size=(N,D)); X+=g[:,None]*2.0*u
 y=((X@t+r.normal(0,.8,N))>0).astype(int)
 return X,g,y

def fit_probe(Xtr,Xte,gtr,gte,ytr,yte):
 lg=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000)).fit(Xtr,gtr)
 rg=make_pipeline(StandardScaler(),SVC(kernel='rbf',C=1,probability=True)).fit(Xtr,gtr)
 ly=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000)).fit(Xtr,ytr)
 sg=lg.predict_proba(Xte)[:,1]; sr=rg.predict_proba(Xte)[:,1]; sy=ly.predict_proba(Xte)[:,1]
 return dict(aucg=oa(gte,sg), bag=balanced_accuracy_score(gte,sg>=.5), rbf=oa(gte,sr), aucy=roc_auc_score(yte,sy))

def setup(Xs,gs):
 xt=torch.from_numpy(Xs.astype(np.float32)); gt=torch.from_numpy(gs.astype(np.int64))
 er=LeaceEraser.fit(xt,gt); P=er.P.detach().cpu().numpy(); b=er.bias.detach().cpu().numpy()
 c=Xs[gs==1].mean(0)-Xs[gs==0].mean(0); c/=max(np.linalg.norm(c),1e-12)
 s=Xs@c; m0=mode1d(s[gs==0]);m1=mode1d(s[gs==1]);target=.5*(m0+m1)
 return P,b,c,target,s

def sparse(X,u,target,groups,score,Kfrac,lam):
 out=X.copy(); idxs=[]
 for g in (0,1):
  ii=np.flatnonzero(groups==g)
  k=max(1,int(round(Kfrac*len(X)/4))) if Kfrac<1 else len(ii)
  order=ii[np.argsort(np.abs(score[ii]-target))[::-1]]; sel=order[:min(k,len(order))]; idxs.extend(sel.tolist())
  d=score[sel]-target; out[sel]=out[sel]-lam*d[:,None]*u[None,:]
 return out,np.array(idxs,int)

rows=[]
for seed in SEEDS:
 X,g,y=data(seed); idx=np.arange(N); train,test=train_test_split(idx,test_size=TEST,random_state=seed,stratify=g)
 space,probe=train_test_split(train,test_size=.35,random_state=seed+1000,stratify=g[train])
 Xs=X[space]; gs=g[space]; ys=y[space]
 P,b,u,target,s=setup(Xs,gs); Xfull_tr=(Xs-b)@P.T+b; full_test=(X[test]-b)@P.T+b; score_test=X[test]@u
 raw=fit_probe(Xs,X[test],gs,g[test],ys,y[test]); full=fit_probe(Xfull_tr,full_test,gs,g[test],ys,y[test])
 rows.append(dict(seed=seed,method='raw',kfrac=0.0,lam=0.0,**raw)); rows.append(dict(seed=seed,method='full_leace',kfrac=1.0,lam=1.0,**full))
 for kf in KFRACS:
  for lam in LAMBDAS:
   Xt,seltr=sparse(Xs,u,target,gs,s,kf,lam); Xv,selte=sparse(X[test],u,target,g[test],score_test,kf,lam)
   met=fit_probe(Xt,Xv,gs,g[test],ys,y[test])
   rows.append(dict(seed=seed,method='sparse',kfrac=kf,lam=lam,nsel_train=len(seltr),nsel_test=len(selte),target=target,**met))

agg=[]
raw_rows=[r for r in rows if r['method']=='raw']
for meth,kf,lam in [('raw',0,0),('full_leace',1,1)]+[('sparse',k,l) for k in KFRACS for l in LAMBDAS]:
 sub=[r for r in rows if r['method']==meth and abs(r['kfrac']-kf)<1e-12 and abs(r['lam']-lam)<1e-12]
 if not sub: continue
 def vals(key): return np.array([r[key] for r in sub],float)
 dY=vals('aucy')-np.array([r['aucy'] for r in raw_rows]); dG=vals('aucg')-np.array([r['aucg'] for r in raw_rows])
 agg.append(dict(method=meth,kfrac=kf,lam=lam,aucg_mean=float(vals('aucg').mean()),aucg_std=float(vals('aucg').std(ddof=1)),aucy_mean=float(vals('aucy').mean()),aucy_std=float(vals('aucy').std(ddof=1)),delta_aucg_mean=float(dG.mean()),delta_aucy_mean=float(dY.mean()),p_aucg=float(wilcoxon(dG).pvalue) if np.any(dG) else 1.0,p_aucy=float(wilcoxon(dY).pvalue) if np.any(dY) else 1.0))
rawm=next(a for a in agg if a['method']=='raw'); cand=[a for a in agg if a['method']!='raw' and a['aucg_mean']<rawm['aucg_mean'] and a['aucy_mean']>=rawm['aucy_mean']]
cand=sorted(cand,key=lambda a:(-a['aucy_mean'],a['aucg_mean']))
summary={'experiment':'M2-LEACE-SPARSE-PARETO-20260814','seeds':SEEDS,'N':N,'D':D,'KFRACS':KFRACS,'LAMBDAS':LAMBDAS,'raw':rawm,'full_leace':next(a for a in agg if a['method']=='full_leace'),'pareto_candidates':cand,'aggregate':agg}
json.dump(rows,(OUT/'rows.json').open('w'),indent=2);json.dump(summary,(OUT/'summary.json').open('w'),indent=2)
with (OUT/'aggregates.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(agg[0].keys()));w.writeheader();w.writerows(agg)
for p in OUT.iterdir():
 if p.is_file(): print(p.name,hashlib.sha256(p.read_bytes()).hexdigest())
print(json.dumps(summary['pareto_candidates'][:10],indent=2)); print('RAW',rawm); print('FULL',summary['full_leace'])
