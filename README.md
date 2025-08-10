# TheTalosPrincible

### showreel
<img width="615" height="621" alt="Screenshot from 2025-08-01 07-16-20" src="https://github.com/user-attachments/assets/5f35180c-7d66-4069-8f70-e0bb75000664" />
<img width="615" height="621" alt="bigwig" src="https://github.com/user-attachments/assets/c92d36c6-e672-42d4-9ded-96013181eb09" />
<img width="615" height="621" alt="Screenshot from 2025-08-01 07-18-21" src="https://github.com/user-attachments/assets/76e1d1da-2c7d-45b0-9616-9b70b0441aee" />
<img width="615" height="621" alt="Screenshot from 2025-08-01 09-36-47" src="https://github.com/user-attachments/assets/1037c594-696e-481f-abd3-c9bb84081c2a" />
<img width="1445" height="1151" alt="Screenshot from 2025-08-01 09-44-17" src="https://github.com/user-attachments/assets/c340254e-0379-4265-99fd-afb1bbea4868" />


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
