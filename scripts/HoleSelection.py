## Script to manually select events from individual sieve holes based
## on their projections onto the GEMs
## Written October 8th 2024
## Kate Evans kate.evans4444@gmail.com


#import modules
import math
import uproot
import configparser as cfg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from polygon_selector_demo import SelectFromCollection
from scipy.stats import gaussian_kde
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

import OPTICS

def main(cfg_file):

    optics = OPTICS.OPTICS()

    config = cfg.ConfigParser()
    config.read(cfg_file)

    #print(config.sections())

    #set variables from config file
    pass_var = config['variable']['pass']
    target_var = config['variable']['target']
    fieldMap_var = config['variable']['fieldMap']
    generator_var = config['variable']['generator']
    rootfile_name = config['variable']['rootfile']
    rot_angle = config['variable']['rotation']

    #make lists of possible sieve holes, targets, and beam passes
    all_file=["11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73"]
    all_passes=["p1","p2","p3","p4","p5"] #used to be all_targets
    all_tg_loc=["Optics1","Optics2","Optics3","LH2"]

    optics.GenNumpyArray(str(rootfile_name))
    optics.DefineSectors(rot_angle)

    hole_id_var = input("Which hole would you like to select and make a CSV file for? ")

    #define the sector based on which hole you want to look at
    if hole_id_var == "11" or hole_id_var == "12" or hole_id_var == "13":
         optics.SelectOneHole(optics.d['sec1'])
    elif hole_id_var == "21" or hole_id_var == "22" or hole_id_var == "23":
         optics.SelectOneHole(optics.d['sec2'])
    elif hole_id_var == "31" or hole_id_var == "32" or hole_id_var == "33":
         optics.SelectOneHole(optics.d['sec3'])
    elif hole_id_var == "41" or hole_id_var == "42" or hole_id_var == "43":
         optics.SelectOneHole(optics.d['sec4'])
    elif hole_id_var == "51" or hole_id_var == "52" or hole_id_var == "53":
         optics.SelectOneHole(optics.d['sec5'])
    elif hole_id_var == "61" or hole_id_var == "62" or hole_id_var == "63":
         optics.SelectOneHole(optics.d['sec6'])
    elif hole_id_var == "71" or hole_id_var == "72" or hole_id_var == "73":
         optics.SelectOneHole(optics.d['sec7'])

    filename = "output/" + str(fieldMap_var) + "/Pass" + str(pass_var) + "_" + str(target_var) + "/" + str(fieldMap_var) + "_p" + str(pass_var) + "_" + str(target_var) + "_" + str(rot_angle) + "rotation_" + hole_id_var + ".csv"

    #print(filename)

    optics.GenCSV(hole_id_var, filename)


if __name__=='__main__':

    main('scripts/config_files/Pass2_Optics2_elasticC12_Symmetric.ini')
