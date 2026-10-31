#!/usr/bin/env python3
"""Reproduce Table 9 from authentic anonymized 38-site raster overlap counts.

No mining-site coordinates are needed. Original classification and geospatial
site inputs are not distributed in this public statistical release.
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix

SEED = 20261024
BOOTSTRAP_REPS = 2500

def calculate(source):
    df = pd.read_csv(source)
    needed = {'validation_id','pair_id','reference_role','y_true','valid_pixel_count',
      'candidate_pixel_count','agreement_pixel_count','candidate_fraction','agreement_fraction'}
    assert needed.issubset(df.columns), f'Missing columns: {sorted(needed-set(df.columns))}'
    assert len(df)==38 and df.pair_id.nunique()==19
    assert df.reference_role.value_counts().to_dict()=={'MINING_SITE':19,'NONMINING_CONTROL':19}
    assert (df.groupby('pair_id').reference_role.nunique()==2).all()
    assert ((df.valid_pixel_count>0)&(df.agreement_pixel_count<=df.candidate_pixel_count)&
            (df.candidate_pixel_count<=df.valid_pixel_count)).all()
    assert np.allclose(df.candidate_fraction,df.candidate_pixel_count/df.valid_pixel_count,atol=1e-10)
    assert np.allclose(df.agreement_fraction,df.agreement_pixel_count/df.valid_pixel_count,atol=1e-10)
    indices = np.random.default_rng(SEED).integers(0,19,size=(BOOTSTRAP_REPS,19))
    y=np.r_[np.ones(19,dtype=int),np.zeros(19,dtype=int)]
    rows=[]; matrices=[]
    for col,label in [('candidate_fraction','Candidate union (SAM or MTMF)'),('agreement_fraction','SAM–MTMF agreement')]:
        t=df.pivot(index='pair_id',columns='reference_role',values=col).sort_index()
        m=t['MINING_SITE'].to_numpy(); c=t['NONMINING_CONTROL'].to_numpy()
        scores=np.r_[m,c]
        mean_boot=(m[indices]-c[indices]).mean(axis=1)*100
        auc_boot=np.empty(BOOTSTRAP_REPS); ap_boot=np.empty(BOOTSTRAP_REPS)
        for j,ii in enumerate(indices):
            sampled=np.r_[m[ii],c[ii]]
            auc_boot[j]=roc_auc_score(y,sampled)
            ap_boot[j]=average_precision_score(y,sampled)
        dci=np.quantile(mean_boot,[.025,.975]); aci=np.quantile(auc_boot,[.025,.975]); pci=np.quantile(ap_boot,[.025,.975])
        rows.append({'metric':label,'n_pairs':19,'n_sites':38,'mean_mining_fraction':m.mean(),
            'mean_control_fraction':c.mean(),'mean_paired_difference_pp':(m-c).mean()*100,
            'difference_ci95_low_pp':dci[0],'difference_ci95_high_pp':dci[1],
            'wilcoxon_p':wilcoxon(m,c,alternative='two-sided',zero_method='pratt').pvalue,
            'roc_auc':roc_auc_score(y,scores),'roc_auc_ci95_low':aci[0],
            'roc_auc_ci95_high':aci[1],'average_precision':average_precision_score(y,scores),
            'ap_ci95_low':pci[0],'ap_ci95_high':pci[1]})
        for rule,pred in [('Any overlap (>0)',scores>0),('At least 10% cover',scores>=.10)]:
            tn,fp,fn,tp=confusion_matrix(y,pred.astype(int),labels=[0,1]).ravel()
            matrices.append({'metric':label,'rule':rule,'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp)})
    return pd.DataFrame(rows),pd.DataFrame(matrices)

def verify(t,c):
    expected={
      'roc_auc':([.766,.602],.0005), 'average_precision':([.687,.588],.0005),
      'wilcoxon_p':([.0067,.241],.0005), 'mean_paired_difference_pp':([23.53,8.25],.005),
      'difference_ci95_low_pp':([7.04,-2.72],.005),
      'difference_ci95_high_pp':([39.24,21.74],.005),
      'roc_auc_ci95_low':([.619,.488],.0005), 'roc_auc_ci95_high':([.900,.711],.0005),
      'ap_ci95_low':([.568,.502],.0005), 'ap_ci95_high':([.895,.711],.0005),
    }
    for name,(values,tol) in expected.items():
        actual=t[name].to_numpy()
        if not np.allclose(actual,values,atol=tol,rtol=0):
            raise AssertionError(f'{name} mismatch: actual {actual}, expected {values}')
    assert c[['TN','FP','FN','TP']].values.tolist()==[
      [16,3,5,14],[16,3,7,12],[17,2,13,6],[17,2,14,5]
    ], 'Confusion matrix mismatch'
    return True

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',default='Site_level_overlap_results.csv')
    p.add_argument('--out',default='.')
    a=p.parse_args()
    t,c=calculate(a.input)
    verify(t,c)
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    t.to_csv(out/'Reproduced_Table9_Statistics.csv',index=False)
    c.to_csv(out/'Reproduced_Table9_Confusion_Matrices.csv',index=False)
    print('PASS: All reported Table 9 figures, intervals and matrices reproduced at published precision.')
    print(t.round(4).to_string(index=False))
    print(c.to_string(index=False))
