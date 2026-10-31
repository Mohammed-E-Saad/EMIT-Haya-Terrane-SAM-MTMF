# Verification and reproducibility status (31 October 2026)

## PASS: authentic independent recalculation of manuscript Table 9

Reprojected the supplied original 38 spatial validation buffers (WGS 84 / UTM 37N) to the ENVI classification raster's geographic CRS, extracted one classified image per buffer using pixel-centre inclusion, and computed **38 authentic coverage observations**. All 19 pairs are retained.

The supplied ENVI header describes 882 × 550 pixels (485,100), geographic WGS 84 with 0.00054223-degree cell size. The binary classification image contains exactly 475,438 class-0, 8,031 class-1 and 1,631 class-2 pixels. Union count = 9,662 pixels.

### Independent point estimates and reported-confidence intervals

| Measure | Candidate union | SAM–MTMF agreement |
|---|---:|---:|
| Mining mean cover | 33.9% | 12.8% |
| Nonmining mean cover | 10.4% | 4.6% |
| Paired difference, pp (95% CI) | 23.53 (7.04, 39.24) | 8.25 (-2.72, 21.74) |
| Wilcoxon two-sided p | 0.0067 | 0.241 |
| ROC AUC (95% CI) | 0.766 (0.619, 0.900) | 0.602 (0.488, 0.711) |
| Average precision (95% CI) | 0.687 (0.568, 0.895) | 0.588 (0.502, 0.711) |
| Any overlap TN/FP/FN/TP | 16/3/5/14 | 17/2/13/6 |
| >=10% TN/FP/FN/TP | 16/3/7/12 | 17/2/14/5 |

All numbers above are independently obtained from original data and agree with manuscript Table 9 **after rounding to the manuscript reporting precision**. CI procedure: 2,500 resamples of 19 intact mining/control pairs, numpy default RNG seed 20261024, percentile intervals. Two-sided Wilcoxon uses Pratt zero convention. Changing seed, resampling scheme, or zero convention can change intervals/p values.

## Boundaries of the reproduction

- **Complete:** all site-level statistical results in Table 9, including interval estimates and confusion counts, from 38 authentic observations.
- **Complete:** raster class counts and actual original spatial-buffer extraction, verified privately from original GeoPackage and final ENVI `.dat` + `.hdr`.
- **Not public in this ZIP:** coordinates and the original 38 geospatial buffers, to avoid exposing mining-site reference locations without reviewed permission; raw georeferenced raster is also excluded. Thus independent *spatial re-extraction* is conditional on obtaining legitimate inputs.
- **Not claimed:** full EMIT-to-map spectral processing or a full independent regeneration of all manuscript figures and results. S1 and S3 are aggregate summaries.
- **Status:** the ZIP is **ready for review/upload**, not proof of an online public release, and no Zenodo DOI is claimed.
