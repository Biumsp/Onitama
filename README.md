# Onitama
This is a basic Python package with GUI to play Onitama.<br/>
The implemented features are:
- The interactive board 
- The engine with tunable search-depth

The engine uses a vanilla MinMax algorithm with alpha-beta pruning.

### Cloning this repository to your local machine
You can clone this repository using the command `git clone https://github.com/Biumsp/Onitama.git` in the GIT bash or by downloading the zip file from this GitHub page.
Be sure to run the codes in a properly set virtual environment.

### Setting up the virtual environment
To use this repository on your local machine you need a properly set Python virtual environment (venv).
All the needed libraries are listed in the `requirements.txt` file.
To install those libraries directly from the file you need to follow these steps (from cmd):
- Create a virtual environment using the command `python -m venv path\environment_name`
- Run the command `> pip install -r path\requirements.txt`
- Activate the virtual environment using `> path\environment_name\scripts\activate`
- Run the scripts from cmd in the active venv

For more info about the virtual environments refer to the [official Python docs](https://docs.python.org/3/library/venv.html)

### Running the codes
On windows:<br/>
Games are started from the terminal. 
- Open the terminal
- Navigate to the parent directory of the repository (e.g., if the path of the repo is **C:\Desktop\onitama**, run `> cd C:\Desktop` in the terminal)
- Run the **main.py** script of the package: `> python -m onitama.main'
