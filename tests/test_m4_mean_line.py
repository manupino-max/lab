import numpy as np
from experiments.m4_mean_line_gaussian import run

def test_mean_line_midpoint_is_exactly_equalized():
    rng=np.random.default_rng(42); n=600; d=12
    g=np.r_[np.zeros(n//2,dtype=int),np.ones(n//2,dtype=int)]
    y=(rng.normal(size=n)+0.8*g>0).astype(int)
    X=rng.normal(size=(n,d)); X[g==1,0]+=2.0; X[g==1,1]-=1.0
    Xtr,Xte=X[:480],X[480:]; gtr,gte=g[:480],g[480:]; ytr,yte=y[:480],y[480:]
    r,_,_=run(Xtr,gtr,ytr,Xte,gte,yte,seed=42)
    mid=r[r.lambda_==0.5]
    endpoint=mid[mid.alpha==1.0].iloc[0]
    assert endpoint.mean_gap < 1e-10

def test_experiment_has_full_line_and_partial_path():
    rng=np.random.default_rng(7); n=400; d=8
    g=rng.integers(0,2,n); y=(rng.normal(size=n)+g>0).astype(int); X=rng.normal(size=(n,d)); X[g==1]+=0.7
    r,_,_=run(X[:300],g[:300],y[:300],X[300:],g[300:],y[300:],seed=7)
    assert set(np.round(r.lambda_.unique(),2))=={0,.25,.5,.75,1}
    assert len(r.alpha.unique())==21
    assert r.shape[0]==105
