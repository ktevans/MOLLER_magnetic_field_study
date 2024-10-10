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

def main(variable, cfg_file):

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

    hole_id_list = ["11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73"]
    beam_pass_list = ["p1","p2","p3","p4","p5"]
    target_list = ["Optics1","Optics2","Optics3","LH2"]

    #df = pd.DataFrame()
    df = pd.read_csv("output/" + str(fieldMap_var) + "/Pass" + str(pass_var) + "_" + str(target_var) + "/" + str(fieldMap_var) + "_p" + str(pass_var) + "_" + str(target_var) + "_all.csv")

    #/Users/ktevans/Documents/GraduateResearch/MOLLER_magnetic_field_study/output/Symmetric/Pass2_Optics2/Symmetric_p2_Optics2_all.csv

    #for hole in hole_id_list:
        #for

    if variable == "theta":
        X = df.iloc[:,[7,8]].values
        #print(X)
        y = df.iloc[:,[3]].values
        degree = 2
    if variable == "sieve_r":
        X=all_df.iloc[:,[7,8]].values
        y=all_df.iloc[:,[12]].values
        degree = 2
    if variable == "phi":
        X=all_df.iloc[:,[7,8,9,10]].values
        y=all_df.iloc[:,[4]].values
        degree = 2
    if variable == "momentum":
        X=all_df.iloc[:,[7,8]].values
        y=all_df.iloc[:,[5]].values
        degree = 3


    fit_parameters_file = "output/" + str(fieldMap_var) + "/Pass" + str(pass_var) + "_" + str(target_var) + "/" + str(fieldMap_var) + "_p" + str(pass_var) + "_" + str(generator_var) + "_" + str(target_var) + "_" + str(rot_angle) + "rotation_" + variable + "_parameters.txt"

    #PolynomialRegression(self, X, y, degree, variable, fit_filename)

    optics.PolynomialRegression(X, y, degree, variable, fit_parameters_file)

if __name__ == '__main__':

    main("theta", 'scripts/config_files/Pass2_Optics2_elasticC12_Symmetric.ini')
