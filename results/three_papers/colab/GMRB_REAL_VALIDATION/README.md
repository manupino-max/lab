# GMR-B / DGTLB — Real-Data Validation

This directory is reserved for reproducible real-data validation runs generated from Google Colab.

The Colab workspace is persistent under:

`MyDrive/latent/GMRB_REAL_VALIDATION/`

Each run is stored under `runs/<RUN_ID>/` and published to this repository under:

`results/three_papers/colab/GMRB_REAL_VALIDATION/<RUN_ID>/`

The runner freezes the reference commit, records environment/configuration, computes SHA-256 checksums, creates a ZIP archive, and excludes credentials and raw datasets from Git publication.

Scientific results are not considered confirmed merely because the runner completes. The final interpretation must use the recorded statistical controls and preserve negative/partial findings.
