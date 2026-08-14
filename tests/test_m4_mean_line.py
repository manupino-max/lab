import numpy as np
from experiments.m4_mean_line_gaussian import run

def test_mean_line_midpoint_is_exactly_equalized():
    rng=np.random.default_rng(42); n0=n1=300; d=12
    g=np.r_[np.zeros(n0,dtype=int),np.ones(n1,dtype=int)]
    y=(rng.normal(size=n0+n1)+0.8*g>0).astype(int)
    X=rng.normal(size=(n0+n1,d)); X[g==1,0]+=2.0; X[g==1,1]-=1.0
    # Stratified deterministic split: both protected groups occur in train and test.
    tr=np.r_[np.arange(0,240),np.arange(300,540)]; te=np.r_[np.arange(240,300),np.arange(540,600)]
    r,_,_=run(X[tr],g[tr],y[tr],X[te],g[te],y[te],seed=42)
    mid=r[np.isclose(r.lambda_,0.5)]
    endpoint=mid[np.isclose(mid.alpha,1.0)].iloc[0]
    assert endpoint.mean_gap < 1e-10

def test_experiment_has_full_line_and_partial_path():
    rng=np.random.default_rng(7); n0=n1=200; d=8
    g=np.r_[np.zeros(n0,dtype=int),np.ones(n1,dtype=int)]; y=(rng.normal(size=n0+n1)+g>0).astype(int); X=rng.normal(size=(n0+n1,d)); X[g==1]+=0.7
    tr=np.r_[np.arange(0,150),np.arange(200,350)]; te=np.r_[np.arange(150,200),np.arange(350,400)]
    r,_,_=run(X[tr],g[tr],y[tr],X[te],g[te],y[te],seed=7)
    assert set(np.round(r.lambda_.unique(),2))=={0,.25,.5,.75,1}
    assert len(r.alpha.unique())==21
    assert r.shape[0]==105
