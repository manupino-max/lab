"""M4 LEACE-CL real-representation experiment on MILK10k.

Exact unconditional map:
    d = mu1-mu0
    w = Sw^{-1} d
    P = d w^T / (w^T d)
    T_a(z) = z - a P(z-mu_f), mu_f=(mu0+mu1)/2.

The protected label is used only to fit train statistics. The transform itself
is unconditional at application time and is applied identically to every test
sample. A fresh downstream task model and protected probe are fitted on each
transformed training representation; test labels are never used for fitting.
"""
from __future__ import annotations
import hashlib, json, platform, time, zipfile
from pathlib import Path
import numpy as np, pandas as pd, requests, torch
from bs4 import BeautifulSoup
from PIL import Image
from transformers import AutoImageProcessor, AutoModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score, roc_auc_score

SEED=42
np.random.seed(SEED)
rng=np.random.default_rng(SEED)
ROOT=Path('/tmp/m4_leace_cl'); OUT=Path('m4_leace_cl_evidence'); ROOT.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
URL='https://isic-archive.s3.amazonaws.com/dois/10.34970-648456/milk10k.zip'
t0=time.time()
zpath=ROOT/'milk10k.zip'
r=requests.get(URL,timeout=600); r.raise_for_status(); zpath.write_bytes(r.content)
bundle_sha=hashlib.sha256(zpath.read_bytes()).hexdigest()
with zipfile.ZipFile(zpath) as z: z.extractall(ROOT/'images')
soup=BeautifulSoup(requests.get('https://api.isic-archive.com/doi/milk10k/',timeout=60).text,'html.parser')
urls=[]
for a in soup.find_all('a'):
    u=a.get('href') or ''
    if 'isic-archive.s3.amazonaws.com' in u and u.lower().split('?')[0].endswith('.csv'): urls.append(u)
urls=list(dict.fromkeys(urls)); frames=[]
for i,u in enumerate(urls):
    rr=requests.get(u,timeout=180); rr.raise_for_status(); p=ROOT/f'src{i}.csv'; p.write_bytes(rr.content); frames.append(pd.read_csv(p))
def norm(s):
    import re; return re.sub(r'[^a-z0-9]+','_',str(s).lower()).strip('_')
def find(df,*names):
    ns={norm(x) for x in names}; return next((c for c in df.columns if norm(c) in ns),None)
tone_df=next(d for d in frames if find(d,'lesion_id') and find(d,'skin_tone_class'))
tl,tc=find(tone_df,'lesion_id'),find(tone_df,'skin_tone_class')
tone=tone_df[[tl,tc]].copy(); tone['_tone']=pd.to_numeric(tone[tc],errors='coerce'); tone=tone.drop_duplicates(tl)
clsset={'akiec','bcc','ben_oth','bkl','df','inf','mal_oth','mel','nv','sccka','vasc'}
dg=next(d for d in frames if find(d,'lesion_id') and sum(norm(c) in clsset for c in d.columns)>=5)
gl=find(dg,'lesion_id'); cls=[c for c in dg.columns if norm(c) in clsset]
gg=dg[[gl]+cls].copy()
for c in cls: gg[c]=pd.to_numeric(gg[c],errors='coerce').fillna(0)
gg['_diagnosis']=gg[cls].idxmax(1); gt=gg[[gl,'_diagnosis']]
base=next(d for d in frames if find(d,'isic_id') and find(d,'lesion_id')); il,bl=find(base,'isic_id'),find(base,'lesion_id')
df=base[[il,bl]].astype(str).merge(tone[[tl,'_tone']].astype({tl:str}),left_on=bl,right_on=tl,how='left').merge(gt.astype({gl:str}),left_on=bl,right_on=gl,how='left')
lesions=np.array(sorted(df[bl].unique()),dtype=object); rng.shuffle(lesions); n=len(lesions); ntr=int(.70*n); nva=int(.15*n)
split={k:('train' if i<ntr else 'val' if i<ntr+nva else 'test') for i,k in enumerate(lesions)}
lesion=df[[bl,'_tone','_diagnosis']].drop_duplicates(bl).rename(columns={bl:'lesion_id'}); lesion['dark']=(lesion['_tone']<=2).astype(int); lesion['split']=lesion.lesion_id.map(split)
assert len(lesion)==5240, len(lesion)
imap={p.stem.casefold():p for p in (ROOT/'images').rglob('*') if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.png','.webp'}}
ids=[]
for _,q in df[[il,bl]].drop_duplicates().iterrows():
    p=imap.get(str(q[il]).casefold())
    if p is not None: ids.append((str(q[bl]),p))
proc=AutoImageProcessor.from_pretrained('facebook/dinov2-base'); model=AutoModel.from_pretrained('facebook/dinov2-base').eval(); device='cuda' if torch.cuda.is_available() else 'cpu'; model.to(device)
acc={}; bs=32
for i in range(0,len(ids),bs):
    chunk=ids[i:i+bs]; ims=[Image.open(p).convert('RGB') for _,p in chunk]
    with torch.no_grad(): z=model(**proc(images=ims,return_tensors='pt').to(device)).last_hidden_state[:,0].cpu().numpy()
    for (lid,_),v in zip(chunk,z): acc.setdefault(lid,[]).append(v)
rows=[]
for lid,v in acc.items():
    q=lesion[lesion.lesion_id==lid].iloc[0]; rows.append((lid,q['split'],float(q['_tone']),int(q['dark']),str(q['_diagnosis']),*np.mean(v,axis=0)))
cols=['lesion_id','split','skin_tone','dark','diagnosis']+[f'z{i}' for i in range(768)]; e=pd.DataFrame(rows,columns=cols); zc=cols[5:]
tr=e[e.split=='train'].copy(); te=e[e.split=='test'].copy(); Xtr=tr[zc].to_numpy(float); Xte=te[zc].to_numpy(float); gtr=tr.dark.to_numpy(int); gte=te.dark.to_numpy(int); ytr=tr.diagnosis.to_numpy(); yte=te.diagnosis.to_numpy()
mu0=Xtr[gtr==0].mean(0); mu1=Xtr[gtr==1].mean(0); d=mu1-mu0; sw=np.cov(Xtr[gtr==0],rowvar=False)*(sum(gtr==0)-1)+np.cov(Xtr[gtr==1],rowvar=False)*(sum(gtr==1)-1); sw/=max(len(Xtr)-2,1); sw+=1e-6*np.eye(Xtr.shape[1]); w=np.linalg.solve(sw,d); denom=float(w@d); P=np.outer(d,w)/denom; muf=.5*(mu0+mu1)
assert np.linalg.norm(P@d-d)<1e-8

def transform(X,a): return X-a*((X-muf)@P.T)
def fairness(y_true,y_pred,g):
    # multiclass macro gaps: average absolute group gap over class-wise rates.
    classes=np.unique(y_true); dp=[]; tpr=[]; tnr=[]
    for c in classes:
        pred=(y_pred==c); truth=(y_true==c)
        rates=[]; tprs=[]; tnrs=[]
        for gg0 in (0,1):
            m=g==gg0; rates.append(pred[m].mean()); tprs.append(pred[m][truth[m]].mean() if truth[m].any() else np.nan); tnrs.append((~pred[m][~truth[m]]).mean() if (~truth[m]).any() else np.nan)
        dp.append(abs(rates[1]-rates[0])); tpr.append(abs(tprs[1]-tprs[0])); tnr.append(abs(tnrs[1]-tnrs[0]))
    return float(np.nanmean(dp)),float(np.nanmean(tpr)),float(np.nanmean(tnr))

def run(a):
    Ttr=transform(Xtr,a); Tte=transform(Xte,a)
    task=LogisticRegression(max_iter=2500).fit(Ttr,ytr); yp=task.predict(Tte)
    probe=LogisticRegression(max_iter=2500).fit(Ttr,gtr); ps=probe.predict_proba(Tte)[:,1]
    dp,tpr,tnr=fairness(yte,yp,gte)
    auc=max(roc_auc_score(gte,ps),1-roc_auc_score(gte,ps))
    m0=Tte[gte==0].mean(0); m1=Tte[gte==1].mean(0)
    return dict(alpha=float(a),mean_gap=float(np.linalg.norm(m1-m0)),protected_auc=float(auc),protected_accuracy=float(accuracy_score(gte,probe.predict(Tte))),dp_gap=dp,equal_opportunity_gap=tpr,tnr_gap=tnr,accuracy=float(accuracy_score(yte,yp)),macro_f1=float(f1_score(yte,yp,average='macro')),balanced_accuracy=float(balanced_accuracy_score(yte,yp)))
res=pd.DataFrame([run(float(a)) for a in np.linspace(0,1,21)]); res.to_csv(OUT/'curve.csv',index=False)
r0=res.iloc[0]; r1=res.iloc[-1]
summary={'status':'M4_LEACE_CL_MILK10K','formula':'T_alpha(z)=z-alpha*P(z-mu_f)','P_d_error':float(np.linalg.norm(P@d-d)),'train_mean_gap_before':float(np.linalg.norm(mu1-mu0)),'train_mean_gap_alpha1':float(np.linalg.norm(transform(Xtr,1)[gtr==1].mean(0)-transform(Xtr,1)[gtr==0].mean(0))),'test_mean_gap_alpha1':float(r1.mean_gap),'baseline':r0.to_dict(),'alpha1':r1.to_dict(),'best_f1_loss_le_0.005':res.loc[(res.macro_f1>=r0.macro_f1-.005)].sort_values(['protected_auc','macro_f1']).iloc[0].to_dict(),'n_lesions':len(e),'n_train':len(tr),'n_test':len(te),'d':768,'seed':SEED,'bundle_sha256':bundle_sha,'device':device,'runtime_seconds':time.time()-t0,'environment':{'python':platform.python_version(),'numpy':np.__version__,'torch':torch.__version__}}
json.dump(summary,open(OUT/'summary.json','w'),indent=2); print(json.dumps(summary,indent=2))
