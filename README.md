# TheTalosPrincible

## for developers
### 27.7.2025 — Update by Noadrow

Hey everyone,
This is a new and refined version of the Talos Principle Project.

The flow/pipeline now depends on 2–4 files, as follows:

    Background file (BG): Used to calculate statistical p-values. If no BG file is provided, the Data file will be used as the BG (and vice versa).

    Target files (1–2): These define your regions of interest. Currently, Venn diagram support between targets works for string data only (IDs, gene names, etc.).

    Data file: This is where the magic happens! The Data file can contain either numerical values or strings — the pipeline will adapt accordingly.
    Note: If no Data file is given, the program will try to use the BG file as the Data source.

👉 Note: The numerical calculation logic is written but still rough — so ignore it for now. Only string-based workflows are fully supported.
### ✅ TODO

    Add an option to save results (including exporting the overlapping subset as a text file for enrichment).

    Fix and improve the numerical calculation pipeline.

    Add support for plain text files as targets, not just BED format.

    Enable creating targets by identifying motifs.

## (Possible) Steps for Install
1. clone and install project
    (recommended for pycharm users) [create venv](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#env-requirements)
2. install requirements (recommended using [requirements.txt](https://www.freecodecamp.org/news/python-requirementstxt-explained/)

### using requirements.txt file, for those using command line:

#### install all packages using command in cli
`pip install -r requirements.txt`

#### update requirements.txt using command in cli
`pip freeze > requirements.txt`

