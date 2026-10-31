# AES16883 | EMIT SAM–MTMF spatial validation | VERIFIED dataset

**Associated manuscript:** *An EMIT-Based SAM–MTMF Workflow for Alteration-Related Exploration Targeting and Matched-Site Validation in the Haya Terrane, NE Sudan*  
**Journal:** Journal of African Earth Sciences  
**Manuscript ID:** AES16883  
**Data verification:** 31 October 2026

## What is independently reproducible?

**The site-level validation results reported in manuscript Table 9 are independently reproduced** from actual non-geolocated pixel-overlap measurements for 19 lithology-matched mining/control pairs (38 sites): the means, paired differences, Wilcoxon p-values, ROC AUC, average precision, two operational confusion matrices and 95% bootstrap intervals agree with the manuscript to its reporting precision. This is a verification of the *site-level validation*, **not** a complete reprocessing of EMIT Level-2A imagery from raw spectra.

## Authentic research data and files

| File | Description |
|---|---|
| `Site_level_overlap_results.csv` | **Actual 38-site measurements** extracted from the final classified mask and 120 m buffers. Coordinates and identifying descriptions excluded; matching pair IDs preserved. |
| `reproduce_table9.py` | Independently repeats every statistical analysis and checks against published Table 9; exits with an error if numbers disagree. |
| `Statistical_Validation_Verified.ipynb` | Colab/Jupyter notebook for the same calculations. Upload the `.csv` and `.py` alongside it. |
| `Reproduced_Table9_Statistics.csv` | Calculated point estimates and 95% CIs from authentic observations. |
| `Reproduced_Table9_Confusion_Matrices.csv` | Both detection rules for candidate union and agreement. |
| `Raster_Class_Counts.csv` | Original final SAM–MTMF classified map pixel counts: 0=475,438; 1=8,031; 2=1,631. |
| `Table_S1_PPI_Iteration_Sensitivity.csv` | Published PPI aggregate summary. |
| `Table_S2_Site_Level_Discrimination.csv` | Published site-level validation aggregate summary. |
| `Table_S3_Priority_Tier_Sensitivity.csv` | Published priority threshold summary. |
| `extract_site_data_from_gis.py` | Optional locally run code to re-extract site-level fractions **only if authorized GIS reference and original raster are available**. |
| `DATA_AVAILABILITY.md` | Public disclosure status and scope. |
| `REPRODUCIBILITY_STATUS.md` | Verification provenance and limitations. |

## Exact statistical protocol

- Reference groups: 19 mining-disturbance sites and 19 matched non-mining controls, 19 intact pairs.
- Pixel inclusion in 120 m polygons: rasterio mask, `all_touched=False` (pixel centre rule).
- Fractions: candidate union = `(class 1 + class 2) / valid pixel count`; strict agreement = `class 2 / valid pixel count`.
- Wilcoxon: two-sided signed-rank with `zero_method='pratt'`.
- ROC AUC and average precision: 38 site-level continuous coverage fractions.
- Bootstrap: **2,500 intact-pair resamples**, `numpy.random.default_rng(20261024)`, percentile 2.5–97.5% interval. The 19 pair indexes are resampled together, preserving mining/control labels.
- Confusion matrices: any overlap (>0), 10% or greater buffer coverage; order TN/FP/FN/TP.

## Run

Install Python packages: `pip install -r requirements.txt`  
Run from repository root: `python reproduce_table9.py`  
Alternatively open `Statistical_Validation_Verified.ipynb` in Colab and upload the `.py` and `.csv`.

For authorised local raster re-extraction only:
`python extract_site_data_from_gis.py --gpkg /private/path/Mining_Reference_Validation_120m.gpkg --raster /private/path/SAM_MTMF_AgreementScore_v0.dat --out Site_level_overlap_results.csv`.
The matching ENVI `.hdr` must be beside `.dat` with the same basename.

## NASA source imagery

NASA EMIT L2A estimated reflectance (V001); original input granule: `EMIT_L2A_RFL_001_20230606T070445_2315705_015`, acquired 6 June 2023; product DOI: https://doi.org/10.5067/EMIT/EMITL2ARFL.001. Original NASA imagery is not redistributed in this package.

## Disclosure and scope

Coordinates, the exact mining/control polygons, original ENVI classification raster and source spectral processing files are **not included in this public-ready ZIP**. The anonymized 38-site data can independently reproduce Table 9's statistics, but site extraction from the classified image cannot be repeated from this ZIP alone. The apparent agreement with mining disturbance is *not* independent verification of gold mineralization, ore grade, or mineral identity. Confirm any data rights before publishing. No GitHub release or Zenodo DOI has been checked or claimed; add them after publication.
