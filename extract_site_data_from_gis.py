#!/usr/bin/env python3
"""OPTIONAL, LOCAL-ONLY raster re-extraction; private GPKG stays on your computer.

Use only with the original 38-buffer GeoPackage and properly georeferenced
ENVI .dat+.hdr files. Output excludes site coordinates by design.
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping

def extract(gpkg,raster,out):
    buffer=gpd.read_file(gpkg,layer='primary_validation_buffers_120m')
    assert len(buffer)==38 and buffer.pair_id.nunique()==19
    records=[]
    with rasterio.open(raster) as src:
        assert src.crs is not None and src.count==1
        b=buffer.to_crs(src.crs)
        for _,site in b.iterrows():
            clip,_=mask(src,[mapping(site.geometry)],crop=True,indexes=1,all_touched=False,filled=False)
            values=clip.compressed()
            assert len(values)>0
            assert np.isin(values,[0,1,2]).all()
            n=len(values);candidate=int(np.count_nonzero(values>=1));agree=int(np.count_nonzero(values==2))
            records.append(dict(validation_id=site.validation_id,pair_id=site.pair_id,
                reference_role=site.reference_role,y_true=int(site.validation_label),
                valid_pixel_count=n,candidate_pixel_count=candidate,agreement_pixel_count=agree,
                candidate_fraction=candidate/n,agreement_fraction=agree/n))
    df=pd.DataFrame(records).sort_values(['pair_id','y_true'],ascending=[True,False])
    assert df.reference_role.value_counts().to_dict()=={'MINING_SITE':19,'NONMINING_CONTROL':19}
    df.to_csv(out,index=False)
    print('Saved non-geolocated validation observations:',out)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--gpkg',required=True)
    p.add_argument('--raster',required=True)
    p.add_argument('--out',default='Site_level_overlap_results.csv')
    a=p.parse_args()
    extract(a.gpkg,a.raster,a.out)
