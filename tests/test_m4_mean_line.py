import numpy as np
from experiments.m4_mean_line_gaussian import run, line_target, transport

def test_mean_line_midpoint_exactly_equalizes_training_means():
    rng=np.random.default_rng(42); n0=n1=300; d=12
    g=np.r_[np.zeros(n0,dtype=int),np.ones(n1,dtype=int)]
    y=(rng.normal(size=n0+n1)+0.8*g>0).astype(int)
    X=rng.normal(size=(n0+n1,d)); X[g==1,0]+=2.0; X[g==1,1]-=1.0
    tr=np.r_[np.arange(0,240),np.arange(300,540)]; te=np.r_[np.arange(240,300),np.arange(540,600)]
    Xtr,gtr,ytr=X[tr],g[tr],y[tr]; Xte,gte,yte=X[te],g[te],y[te]
    mu0=Xtr[gtr==0].mean(0); mu1=Xtr[gtr==1].mean(0); target=line_target(mu0,mu1,0.5)
    Ttr=transport(Xtr,gtr,mu0,mu1,target,1.0)
    assert np.linalg.norm(Ttr[gtr==0].mean(0)-Ttr[gtr==1].mean(0)) < 1e-10
    r,_,_=run(Xtr,gtr,ytr,Xte,gte,yte,seed=42)
    mid=r[np.isclose(r.lambda_,0.5)]
    assert float(mid[mid.alpha==1.0].mean_gap.iloc[0]) < float(mid[mid.alpha==0.0].mean_gap.iloc[0])

def test_experiment_has_full_line_and_partial_path():
    rng=np.random.default_rng(7); n0=n1=200; d=8
    g=np.r_[np.zeros(n0,dtype=int),np.ones(n1,dtype=int)]; y=(rng.normal(size=n0+n1)+g>0).astype(int); X=rng.normal(size=(n0+n1,d)); X[g==1]+=0.7
    tr=np.r_[np.arange(0,150),np.arange(200,350)]; te=np.r_[np.arange(150,200),np.arange(350,400)]
    r,_,_=run(X[tr],g[tr],y[tr],X[te],g[te],y[te],seed=7)
    assert set(np.round(r.lambda_.unique(),2))=={0,.25,.5,.75,1}
    assert len(r.alpha.unique())==21
    assert r.shape[0]==105
