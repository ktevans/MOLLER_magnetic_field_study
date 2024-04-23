## python version needs to be above 3.6
mkdir venv
python3 -m venv ./venv
source venv/bin/activate.csh
pip3 install uproot3
pip3 install matplotlib
pip3 install pandas
alias python3 venv/bin/python3
