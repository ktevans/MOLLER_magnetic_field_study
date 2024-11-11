# Important Scripts

Most scripts are in python and can be run on the farm or locally either from a terminal or using Jupyter Notebook. The C++ scripts assume access to ROOT and should be run on the farm.

## SlimGeneral.C

This script will take a large root file and output a slimmed root file with only the variables of interest. These variables include:
* "sieve_r" - "hit.r[hit.det==270 && prm_e && hit.trid==main_trid][0]"
* "sieve_ph" - "hit.ph[hit.det==270 && prm_e && hit.trid==main_trid][0]"
* "sieve_x" - "hit.x[hit.det==270 && prm_e && hit.trid==main_trid][0]"
* "sieve_y" - "hit.y[hit.det==270 && prm_e && hit.trid==main_trid][0]"
* "sieve_px" - "hit.px[hit.det==270 && prm_e && hit.trid==main_trid][0]"
* "sieve_py" - "hit.py[hit.det==270 && prm_e && hit.trid==main_trid][0]"
* "sieve_pz" - "hit.pz[hit.det==270 && prm_e && hit.trid==main_trid][0]
* "main_r" - "hit.r[main && prm_e && hit.trid==main_trid][0]"
* "main_ph" - "hit.ph[main && prm_e && hit.trid==main_trid][0]"
* "main_trid" - "hit.trid[main && prm_e][0]"
* "main_x" - "hit.x[main && prm_e && hit.trid==main_trid][0]"
* "main_y" - "hit.y[main && prm_e && hit.trid==main_trid][0]"
* "main_px" - "hit.px[ prm_e && main && hit.trid==main_trid][0]"
* "main_py" - "hit.py[ prm_e && main && hit.trid==main_trid][0]"
* "main_pz" - "hit.pz[ prm_e && main && hit.trid==main_trid][0]"
* "gem1_r" - "hit.r[ prm_e && hit.det==32 && hit.trid==main_trid][0]"
* "gem1_ph" - "hit.ph[ prm_e && hit.det==32 && hit.trid==main_trid][0]"
* "gem1_x" - "hit.x[ prm_e && hit.det==32 && hit.trid==main_trid][0]"
* "gem1_y" - "hit.y[ prm_e && hit.det==32 && hit.trid==main_trid][0]"
* "gem1_px" - "hit.px[ prm_e && hit.det==32 && hit.trid==main_trid][0]"
* "gem1_py" - "hit.py[ prm_e && hit.det==32 && hit.trid==main_trid][0]"
* "gem1_pz" - "hit.pz[ prm_e && hit.det==32 && hit.trid==main_trid][0]"
* "gem4_x" - "hit.x[ prm_e && hit.det==35 && hit.trid==main_trid][0]"
* "gem4_y" - "hit.y[ prm_e && hit.det==35 && hit.trid==main_trid][0]"
* "tg_th" - "part.th[part.trid==main_trid][0]"
* "tg_ph" - "part.ph[part.trid==main_trid][0]"
* "tg_p" - "part.p[part.trid==main_trid][0]"
* "tg_vz" - "part.vz[part.trid==main_trid][0]"
* "rate" - straight from the original root tree

The saved events are all defined as "primary electrons" (prm_e) which meet the conditions "hit.pid==11 && hit.mtrid==0 && hit.trid==1". 
These events are further filtered to only look at primary electrons which hit the main detector.

NOTE: the new root tree is called "newT" instead of "T".

To use this script, use the following commands:
```
root -l
.L scripts/SlimGeneral.C
SlimGeneral("file")
```
Do NOT include the ".root" extension in your input.

## GenHoleCSV.C

This script will take a slimmed root file and generate CSV files for each individual sieve hole. These CSV files are then stored on the farm and can be easily moved to your local computer to work with if you want.

To use this script, use the following commands:
```
root -l
.L scripts/GenHoleCSV.C
GenHoleCSV("file.root",0.0)
```
This will output a root file with all of the plots, a CSV file for each hole, and a PDF with an r vs phi plot of all the selected data.

## HoleSelection.py

## OpticsReconstruction.py

## combineCSV.py

## sieveGoleImageAnalysis.py

## compareMeans.py
