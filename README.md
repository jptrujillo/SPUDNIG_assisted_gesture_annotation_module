## Purpose
This tutorial module is meant to illustrate how you can use video-based motion tracking to assist in the manual coding of hand gestures. The workflow is: <br>
1. Run motion tracking to capture bodily movement
2. Use the SPUDNIG algorithm to automatically detect hand movements and export these to an ELAN file
3. Go through the movement annotations, removing non-gesture movements, keeping gesture movements

## Source
This tutorial makes use of the SPUDNIG algorithm, originally produced by Ripperda, Drijvers & Holler, 2020 ( https://doi.org/10.3758/s13428-020-01350-2), and implemented here based on version 2.0, as can be found on the Open Science Framework: https://osf.io/hqw4s/

## Installation
First, make sure that you have Python installed. Otherwise, download and install: https://www.python.org/downloads/release/python-3120/   <br>

Next, it's recommended that you make a virtual environment and run all code from there (this makes sure that there are no conflicts between different versions of modules, python versions, etc). If you're not familiar with this process, you should open a terminal window within the directory containing this notebook. In Windows, you can right click within the folder and select "Open in terminal". Then, run the following commands to 1) create a virtual environment, 2) activate that environment, and 3) install required dependencies for this module.

<i>py -m venv venv</i> <br>
<i>./venv/Scripts/activate</i> <br>
<i>pip install -r requirements.txt</i> <br>
<br>
Note that you should run Jupyter from within this virtual environment, and open the .ipynb file.<br>
<i> jupyter lab</i>

