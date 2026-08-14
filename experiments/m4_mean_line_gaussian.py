"""Independent M4 mean-line / Gaussian fairness experiment."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score

def line_target(mu0, mu1, lam): return lam * mu0 + (1.0 - lam) * mu1

def transport(X, g, mu0, mu1, target, alpha):
    Y = X.copy(); Y[g == 0] += alpha * (target - mu0); Y[g == 1] += alpha * (target - mu1); return Y

def protected_probe(Xtr,gtr,Xte,gte):
    p=LogisticRegression(max_iter=2000).fit(Xtr,gtr); s=p.predict_proba(Xte)[:,1]; q=p.predict(Xte)
    a=roc_auc_score(gte,s); return float(max(a,1-a)), float(accuracy_score(gte,q))

def task_probe(Xtr,ytr,Xte,yte):
    p=LogisticRegression(max_iter=2000).fit(Xtr,ytr); q=p.predict(Xte)
    return dict(task_accuracy=float(accuracy_score(yte,q)),task_balanced_accuracy=float(balanced_accuracy_score(yte,q)),task_macro_f1=float(f1_score(yte,q,average='macro')))

def symmetric_kl_diag(X0,X1,eps=1e-6):
    m0,m1=X0.mean(0),X1.mean(0); v0,v1=X0.var(0)+eps,X1.var(0)+eps
    a=.5*np.sum(np.log(v1/v0)+(v0+(m0-m1)**2)/v1-1); b=.5*np.sum(np.log(v0/v1)+(v1+(m0-m1)**2)/v0-1); return float((a+b)/2)

def run(Xtr,gtr,ytr,Xte,gte,yte,seed=42):
    np.random.seed(seed); mu0=Xtr[gtr==0].mean(0); mu1=Xtr[gtr==1].mean(0); rows=[]
    for lam in np.linspace(0,1,5):
        target=line_target(mu0,mu1,float(lam))
        for alpha in np.linspace(0,1,21):
            Ttr=transport(Xtr,gtr,mu0,mu1,target,float(alpha)); Tte=transport(Xte,gte,mu0,mu1,target,float(alpha))
            auc,acc=protected_probe(Ttr,gtr,Tte,gte); task=task_probe(Ttr,ytr,Tte,yte)
            rows.append(dict(lambda_=float(lam),alpha=float(alpha),protected_auc=auc,protected_accuracy=acc,mean_gap=float(np.linalg.norm(Tte[gte==1].mean(0)-Tte[gte==0].mean(0))),gaussian_symmetric_kl=symmetric_kl_diag(Tte[gte==0],Tte[gte==1]),**task))
    return pd.DataFrame(rows),mu0,mu1

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',required=True); ap.add_argument('--seed',type=int,default=42); a=ap.parse_args()
    d=np.load(a.input,allow_pickle=True); r,mu0,mu1=run(d['X_train'],d['g_train'],d['y_train'],d['X_test'],d['g_test'],d['y_test'],a.seed)
    o=Path(a.output); o.parent.mkdir(parents=True,exist_ok=True); r.to_csv(o.with_suffix('.csv'),index=False)
    o.with_suffix('.json').write_text(json.dumps({'seed':a.seed,'n_train':len(d['X_train']),'n_test':len(d['X_test']),'dimension':d['X_train'].shape[1],'mean_distance':float(np.linalg.norm(mu1-mu0))},indent=2))
if __name__=='__main__': main()
