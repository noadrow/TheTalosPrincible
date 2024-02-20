# TheTalosPrincible


## for developers
### from 14.2.24 meeting
The collaboration on this project is meant to create a more simple and intuitive tool for researchers.   
The tools available today are mostly cli (command line) based and require many steps even for the simplest query.

Currently, user's action pipline is:
uploading a file --> running macs2 --> running bedtools --> converting file from .bed to .bam --> using macs2 for peak calling --> presenting the results graphically

So the most urgent goals would be:
 - Squashing the pipeline into a single button
 - Allowing the user to choose the parameters for the process in a more efficient and intuitive way
In the future we hope to add feature like:
 - Gene listing (with similar "squashed" action pipline)
 - "Automated" Peak Calling Graphs

Also since we're hoping to work using git&hub, we'll try to incorporate the use of pull request and issue closing in commit messages.
Individual work should be done on the appropriate branches.
The 'for_beginners' branch can be used for new incomers (e.g can be used to update documentation and trying out git features etc.) 


## (Possible) Steps for Install
1. clone and install project
    (recommended for pycharm users) [create venv](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#env-requirements)
2. install requirements (recommended using [requirements.txt](https://www.freecodecamp.org/news/python-requirementstxt-explained/), see more info in the file) 
    check by running `bedtools intersect -a hg19_mir688.bed -b hg19_mir688.bed` (TODO didn't work from cli)
    check by running Round1/round2.py
3. ...



### using requirements.txt file, for those using command line:

#### install all packages using command in cli
`pip install -r requirements.txt`

#### update requirements.txt using command in cli
`pip freeze > requirements.txt`

