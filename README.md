# MOLLER magnetic field study
Collection of scripts that facilitate the study of the magnetic field for the MOLLER experiment using optics analysis

## Setting up your virtual environment
You need python downloaded onto your computer in order to use the python scripts in this repository. Here are resouces to download python:

https://www.python.org/downloads/macos/

https://www.python.org/downloads/windows/

You can also run these scripts directly on a Jupyter Notebook. For example, open your JupyterLab and type:
```
run /path/to/MOLLER_magnetic_field_study/scripts/test.py
```
You should see the output "Hello, World!"

To build the virtual environment on your local computer start in the cloned base directory (MOLLER_magnetic_field_study) and type the following:
```
!/bin/bash
source setup.csh
```

After the first time you set up your virtual environment, you should do the following:
```
!/bin/bash
source sourceme.csh
```
If you need to install more python modules, e.g. pyperclip, use the following command:
```
pip3 install pyperclip
```
In order to test your setup, run the test script by typing:
```
python3 scripts/test.py
```
You should see the output "Hello, World!"
