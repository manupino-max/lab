"""Selective-LEACE multi-seed validation experiment.

Scientific rule:
  train raw classifier once; fit LEACE on TRAIN only; compute
  s_i=|p_raw-p_leace| on validation; selectively replace validation
  representations; keep clf_raw fixed; choose tau only on validation.

No TEST split is created or used in this experiment.
EPS_AUC and EPS_BA are mandatory CLI arguments: they are deliberately
not hard-coded because they were not frozen in the supplied protocol.
"""
import argparse, json, os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (f1_score, roc_auc_score, balanced_accuracy_score,
                             accuracy_score, precision_score, recall_score,
                             average_precision_score, confusion_matrix)
from concept_erasure import LeaceEraser

SEEDS = list(range(20))
TAU_GRID = np.array([0.00,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,
                     0.10,0.12,0.15,0.20], dtype=float)
EPS_F1 = 0.01


def safe_div(a,b): return a/b if b != 0 else np.nan


def group_metrics(y,pred,prob,z):
    out={}
    for g in (0,1):
        m=np.asarray(z)==g; yy=np.asarray(y)[m]; pp=np.asarray(pred)[m]; ss=np.asarray(prob)[m]
        if len(yy)==0: continue
        tn,fp,fn,tp=confusion_matrix(yy,pp,labels=[0,1]).ravel()
        tpr=safe_div(tp,tp+fn); fpr=safe_div(fp,fp+tn)
        fnr=safe_div(fn,fn+tp); ppv=safe_div(tp,tp+fp); npv=safe_div(tn,tn+fn)
        try: auc=roc_auc_score(yy,ss)
        except ValueError: auc=np.nan
        out.update({f'positive_rate_Z{g}':np.mean(pp),f'TPR_Z{g}':tpr,
                    f'FPR_Z{g}':fpr,f'FNR_Z{g}':fnr,f'PPV_Z{g}':ppv,
                    f'NPV_Z{g}':npv,f'F1_Z{g}':f1_score(yy,pp,zero_division=0),
                    f'BA_Z{g}':balanced_accuracy_score(yy,pp),
                    f'AUC_Z{g}':auc,f'mean_score_Z{g}':np.mean(ss)})
    return out


def evaluate(y,pred,prob,z):
    gm=group_metrics(y,pred,prob,z)
    pr0,pr1=gm['positive_rate_Z0'],gm['positive_rate_Z1']
    tpr0,tpr1=gm['TPR_Z0'],gm['TPR_Z1']; fpr0,fpr1=gm['FPR_Z0'],gm['FPR_Z1']
    fnr0,fnr1=gm['FNR_Z0'],gm['FNR_Z1']; ppv0,ppv1=gm['PPV_Z0'],gm['PPV_Z1']; npv0,npv1=gm['NPV_Z0'],gm['NPV_Z1']
    abs_eod=abs(tpr1-tpr0); abs_dp=abs(pr1-pr0); abs_fpr=abs(fpr1-fpr0); abs_fnr=abs(fnr1-fnr0)
    abs_ppv=abs(ppv1-ppv0); abs_npv=abs(npv1-npv0); abs_aod=abs(((tpr1-tpr0)+(fpr1-fpr0))/2)
    abs_eo=max(abs_eod,abs_fpr)
    task={'F1_Y':f1_score(y,pred,zero_division=0),'AUC_Y':roc_auc_score(y,prob),
          'BA_Y':balanced_accuracy_score(y,pred),'accuracy_Y':accuracy_score(y,pred),
          'precision_Y':precision_score(y,pred,zero_division=0),'recall_Y':recall_score(y,pred,zero_division=0),
          'AP_Y':average_precision_score(y,prob)}
    phi_vals=[1-abs_eod,1-abs_dp,1-abs_fpr,1-abs_fnr,1-abs_ppv,1-abs_npv,1-abs_aod,1-abs_eo]
    return {**task,**gm,'Pi':np.mean([task['F1_Y'],task['AUC_Y'],task['BA_Y']]),
            'Phi_EOD':1-abs_eod,'Phi_DP':1-abs_dp,'Phi_FPR':1-abs_fpr,'Phi_FNR':1-abs_fnr,
            'Phi_PPV':1-abs_ppv,'Phi_NPV':1-abs_npv,'Phi_AOD':1-abs_aod,'Phi_EO':1-abs_eo,
            'Phi':np.mean(phi_vals)}


def make_data(seed,n=1200,d=20):
    rng=np.random.default_rng(seed)
    z=rng.binomial(1,0.5,n)
    x=rng.normal(size=(n,d))
    # Controlled group-dependent representation shift plus predictive signal.
    x[:,0]+=1.15*z
    x[:,1]+=0.70*z
    latent=0.9*x[:,2]+0.8*x[:,3]+0.65*z+rng.normal(scale=1.0,size=n)
    y=(latent>np.median(latent)).astype(int)
    idx=rng.permutation(n); cut=int(0.7*n)
    tr,va=idx[:cut],idx[cut:]
    return x[tr],x[va],y[tr],y[va],z[tr],z[va]


def selective(xraw,xleace,mask):
    out=np.asarray(xraw).copy(); out[np.asarray(mask)]=np.asarray(xleace)[np.asarray(mask)]; return out


def run(seed,eps_auc,eps_ba,tau_grid):
    xtr,xva,ytr,yva,ztr,zva=make_data(seed)
    eraser=LeaceEraser.fit(xtr,ztr)
    xtr_l=eraser(xtr); xva_l=eraser(xva)
    clf=LogisticRegression(max_iter=2000,solver='lbfgs')
    clf.fit(xtr,ytr)
    p_raw=clf.predict_proba(xva)[:,1]; p_l=clf.predict_proba(xva_l)[:,1]
    s=np.abs(p_raw-p_l); pred_raw=(p_raw>=0.5).astype(int)
    raw=evaluate(yva,pred_raw,p_raw,zva)
    rows=[]
    for tau in tau_grid:
        mask=s>=tau
        xsel=selective(xva,xva_l,mask)
        p=clf.predict_proba(xsel)[:,1]; pred=(p>=0.5).astype(int)
        sel=evaluate(yva,pred,p,zva)
        dF1=sel['F1_Y']-raw['F1_Y']; dAUC=sel['AUC_Y']-raw['AUC_Y']; dBA=sel['BA_Y']-raw['BA_Y']; dPhi=sel['Phi']-raw['Phi']
        rows.append({'seed':seed,'tau':float(tau),'IR_val':float(mask.mean()),'n_intervened_val':int(mask.sum()),
                     'F1_RAW':raw['F1_Y'],'F1_SEL':sel['F1_Y'],'delta_F1':dF1,
                     'AUC_RAW':raw['AUC_Y'],'AUC_SEL':sel['AUC_Y'],'delta_AUC':dAUC,
                     'BA_RAW':raw['BA_Y'],'BA_SEL':sel['BA_Y'],'delta_BA':dBA,
                     'Pi_RAW':raw['Pi'],'Pi_SEL':sel['Pi'],'Phi_RAW':raw['Phi'],'Phi_SEL':sel['Phi'],'delta_Phi':dPhi,
                     'Phi_EOD_RAW':raw['Phi_EOD'],'Phi_EOD_SEL':sel['Phi_EOD'],
                     'Phi_DP_RAW':raw['Phi_DP'],'Phi_DP_SEL':sel['Phi_DP'],
                     'Phi_FPR_RAW':raw['Phi_FPR'],'Phi_FPR_SEL':sel['Phi_FPR'],
                     'Phi_FNR_RAW':raw['Phi_FNR'],'Phi_FNR_SEL':sel['Phi_FNR'],
                     'Phi_PPV_RAW':raw['Phi_PPV'],'Phi_PPV_SEL':sel['Phi_PPV'],
                     'Phi_NPV_RAW':raw['Phi_NPV'],'Phi_NPV_SEL':sel['Phi_NPV'],
                     'Phi_AOD_RAW':raw['Phi_AOD'],'Phi_AOD_SEL':sel['Phi_AOD'],
                     'Phi_EO_RAW':raw['Phi_EO'],'Phi_EO_SEL':sel['Phi_EO'],
                     'IR_Z0':float(mask[zva==0].mean()),'IR_Z1':float(mask[zva==1].mean()),
                     'mean_s_Z0':float(s[zva==0].mean()),'mean_s_Z1':float(s[zva==1].mean()),
                     'changed_prediction':float((pred_raw!=pred).mean()),
                     'improved':float(((pred_raw!=yva)&(pred==yva)).mean()),
                     'worsened':float(((pred_raw==yva)&(pred!=yva)).mean()),
                     'valid':bool((dPhi>0) and (dF1>=-EPS_F1) and (dAUC>=-eps_auc) and (dBA>=-eps_ba))})
    df=pd.DataFrame(rows)
    valid=df[df.valid].sort_values(['IR_val','tau'])
    if valid.empty: star={'seed':seed,'tau_star':np.nan,'IR_val':np.nan,'delta_F1':np.nan,'delta_AUC':np.nan,'delta_BA':np.nan,'delta_Phi':np.nan,'selection_status':'NO_VALID_TAU'}
    else:
        b=valid.iloc[0]; star={'seed':seed,'tau_star':b.tau,'IR_val':b.IR_val,'delta_F1':b.delta_F1,'delta_AUC':b.delta_AUC,'delta_BA':b.delta_BA,'delta_Phi':b.delta_Phi,'selection_status':'SELECTED'}
    return df,star,raw


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--eps-auc',type=float,required=True)
    ap.add_argument('--eps-ba',type=float,required=True)
    ap.add_argument('--out',default='results/selective_leace_validation')
    args=ap.parse_args()
    if args.eps_auc<0 or args.eps_ba<0: raise ValueError('EPS must be non-negative')
    os.makedirs(args.out,exist_ok=True)
    all_df=[]; stars=[]; raws=[]
    for seed in SEEDS:
        df,star,raw=run(seed,args.eps_auc,args.eps_ba,TAU_GRID); all_df.append(df); stars.append(star)
        raws.append({'seed':seed,'F1_RAW':raw['F1_Y'],'AUC_RAW':raw['AUC_Y'],'BA_RAW':raw['BA_Y'],'Pi_RAW':raw['Pi'],'Phi_RAW':raw['Phi']})
        print(f'SEED {seed:02d}: {star["selection_status"]} tau*={star["tau_star"]} IR={star["IR_val"]} dPhi={star["delta_Phi"]}')
    va=pd.concat(all_df,ignore_index=True); ts=pd.DataFrame(stars); rr=pd.DataFrame(raws)
    va.to_csv(os.path.join(args.out,'validation_all_seeds.csv'),index=False); ts.to_csv(os.path.join(args.out,'tau_star_by_seed.csv'),index=False); rr.to_csv(os.path.join(args.out,'raw_reference.csv'),index=False)
    summary={'n_seeds':20,'seeds':SEEDS,'tau_grid':TAU_GRID.tolist(),'EPS_F1':EPS_F1,'EPS_AUC':args.eps_auc,'EPS_BA':args.eps_ba,
              'test_used':False,'classifier':'LogisticRegression','classifier_fixed_during_selection':True,
              'leace_fit_scope':'TRAIN_ONLY','selection':'minimize IR_val among valid tau; tie=min tau',
              'valid_rule':'delta_Phi > 0 AND delta_F1 >= -EPS_F1 AND delta_AUC >= -EPS_AUC AND delta_BA >= -EPS_BA',
              'selected_rate':float((ts.selection_status=='SELECTED').mean()),
              'median_tau_star':float(ts.tau_star.median()) if ts.tau_star.notna().any() else None,
              'median_IR_val':float(ts.IR_val.median()) if ts.IR_val.notna().any() else None}
    with open(os.path.join(args.out,'validation_protocol.json'),'w') as f: json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
