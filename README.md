# Q-learning Acrobat

CLI-Usage: ./acrobat.py [fast/slow] [Name of file to fill Q-table]

![](./gif/acrbot.mp4)

### CLI-Usage details about sys.argv

sys.argv[1] : can be either 'slow' or 'fast' for running with or without grapics respectively.

sys.argv[2] : if this argument is omitted the game starts with a fresh version of Q-table where all values are initialized to 0.5.
            : Else Q-table is filled with the keys values pair from the file mentioned here. 
            File db20000.txt contains kay values pair from Q-table after 20000 games.
            File db30000.txt contains kay values pair from Q-table after 30000 games.

#### Installation

1. Clone this repo
2. `cd` into project
3. Create a virtual environment `python3 -m venv acrbot`
4. Activate virtual environment `source ./acrbot/bin/activate`
5. install requirments.txt `pip3 install -r requirement.txt` and now you can run `./run.sh`


## To view 1000 games without graphics

(default value of eta = 0.99 Hence the first 400 games are lost)

This example plays 1000 games, when Q-table is populated with previously trained values from file db30000.txt:

Run this:
    python3 ./src/acrobot.py fast ./data/db30000.txt     
OR :
    ./run.sh

## To view 1000 games with graphics

 Run this:
     python3 ./src/acrobot.py slow ./src/db30000.txt 

After 1000 moves the program prints the Q-table values and
average steps per game for last 1000 games


### Saving Q-table db
Run in interactive Python3 and write db variable into txt file.
