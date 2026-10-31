# Data Availability | AES16883

## Original satellite imagery
NASA's EMIT Level-2A estimated reflectance product, version 001, is available from NASA (https://doi.org/10.5067/EMIT/EMITL2ARFL.001). The study input is EMIT_L2A_RFL_001_20230606T070445_2315705_015 (6 June 2023). The NASA granule itself is not redistributed here.

## Dataset made available in this package
This release contains **authentic non-geolocated measurements for all 38 validation sites (19 paired mining/control locations)**, with original pixel counts and both continuous candidate-coverage fractions in `Site_level_overlap_results.csv`. The provided script, notebook, and calculated statistics independently reproduce the site's manuscript Table 9 values, including 2,500-replicate intact-pair bootstrap confidence intervals. Published supplementary aggregate tables S1–S3, final raster class counts, and verification notes are included.

## Materials not deposited in this public-ready package
Reference-site exact geographic coordinates and polygons, final georeferenced raster image, source endmember products, and full scene-processing workflow files are **not included**. The exact GIS locations were used to extract the anonymised coverage values and have been checked locally against the manuscript; decisions regarding redistribution of locations require review. The reproducibility here is **complete for site-level statistics**, but not a full independently executable re-extraction of spatial measurements or a complete regeneration of the spectral classification from original EMIT imagery. This statement does not claim that legal restrictions were verified.

## Repository status
No permanent repository DOI or public access URL has yet been issued or verified. Replace this status with the final repository and DOI only when they exist, and add the corresponding concise Data Availability statement to the submitted manuscript. Do not state the data are publicly accessible until public repository access has actually been enabled.
