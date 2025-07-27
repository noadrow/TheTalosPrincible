# TheTalosPrincible

## for developers
## 27.7.2025 update by noadrow
hey guys this is a new and refined version of the talos princible project 
the flow\pipeline now is dependent on 2-4 files in the following way:
uploading Background file to calculate satistical p-value - if BG was not given the Data file is going to be used as BG and viseversa
uploading 1-2 target files - currently the support for venn diagram between the targets are for string data only (id\genes and stuff)
uploading data file - this is were the magic happens ! the data file can contain a numerical values or strings and the pipeline would be chosen in accordance to that, note that if no data file given the program would try to use the BG file as data 

the numerical calculation is written but it's shit so ignore it, for now only string values are supported 

TODO:
*option to save results. (also output overlap subset as text file for enrichments)
*fix numerical calculation.
*add support for text files and not just bed in target area 
*anable creating targets by identifying motifs


## (Possible) Steps for Install
1. clone and install project
    (recommended for pycharm users) [create venv](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#env-requirements)
2. install requirements (recommended using [requirements.txt](https://www.freecodecamp.org/news/python-requirementstxt-explained/)

### using requirements.txt file, for those using command line:

#### install all packages using command in cli
`pip install -r requirements.txt`

#### update requirements.txt using command in cli
`pip freeze > requirements.txt`

