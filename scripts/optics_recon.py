#import modules
import math
import uproot
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

def main(flag_csv_var, flag_fit_var, pass_value_var, tg_loc_var, flag_histo, fit_theta_var, fit_phi_var, fit_momentum_var, fit_sieve_r_var, filename_var, field_map_var, rot_angle, right_sector):

     #we are using the OPTICS() class
     optics=OPTICS.OPTICS()

     #define lists of all possible input variables. This will need updating for different studies, so some of the lists are commented out.
     all_file=["11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73"]
     ##all_target=["p4","p3", "p2", "p1"]
     all_target=["p1","p2","p3","p4","p5"]
     all_tg_loc=["Optics1","Optics2","Optics3","LH2"]
     ##all_tg_loc=["1DS", "1US", "2DS", "2US", "1", "2", "3"]

     #if the csv variable is flagged, then you want to make a csv file for the specified hole and sector
     if flag_csv_var==1:
         optics.GenNumpyArray(str(filename_var))
         optics.DefineSectors(rot_angle)
         #you can draw a histogram of all the holes at once
         #I commented these out because I never use this so it was taking up time and space
         ##if flag_histo == 1:
             ##optics.DrawHistAllSectors()

         #keep repeating until repeat variable is false
         hole_id_var = ""

         #ask which hole to select and generate csv file for
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

         #define the file name for the output csv and print it
         filename="/volatile/halla/moller12gev/ktevans1/rootfiles2024/MagFieldStudy/" + field_map_var + "/output/" + field_map_var + "_" + pass_value_var + "_" + tg_loc_var + "_"+ str(rot_angle) +"degRot_" + hole_id_var + ".csv"
         ##filename="/volatile/halla/moller12gev/ktevans1/rootfiles2024/OpticsAnalysis/Optics" + tg_loc_var + "/" + field_map_var + "FieldMap_" + tg_loc_var + "_" + pass_value_var + "_" + hole_id_var + ".csv"
         print(filename)

         #generate the csv file for the specified hole
         optics.GenCSV(hole_id_var, filename)
         print("You generated the CSV file!")


     #this flag is 1 if you want to make the reconstruction fit
     if flag_fit_var==1:

      all_df = pd.DataFrame()

      for a_tg_loc in all_tg_loc:
          for a_pass in all_target:
              for a_file in all_file:
                  ##file_new = "/volatile/halla/moller12gev/ktevans1/rootfiles2024/OpticsAnalysis/Optics"+str(a_tg_loc)+"/"+field_map_var+"FieldMap_Optics"+str(a_tg_loc)+"_" + str(a_pass) + "_" + str(a_file)+ ".csv"
                  file_new="/volatile/halla/moller12gev/ktevans1/rootfiles2024/MagFieldStudy/" + field_map_var + "/output/" + field_map_var + "_" + str(a_pass)  + "_" + str(a_tg_loc) + "_" + str(a_file) + ".csv"
                  print(file_new)
                  df_new=pd.read_csv(file_new)
                  all_df = pd.concat([all_df,df_new],axis=0)

                  ##fit_filename = "/volatile/halla/moller12gev/ktevans1/rootfiles2024/OpticsAnalysis/Optics"+str(a_tg_loc)+"/"+field_map_var+"FieldMap_Optics"+tg_loc_var+"_"+pass_value_var+"_"+variable+"_parameters.txt"
                  fit_filename="/volatile/halla/moller12gev/ktevans1/rootfiles2024/MagFieldStudy/" + field_map_var + "/output/" + field_map_var + "_" + str(a_pass)  + "_" + str(a_tg_loc) + "_" + str(a_file) + "_" + variable  + "_parameters.txt"

      #do the theta reconstruction
      if fit_theta_var == 1:
          variable = "theta"
          X=all_df.iloc[:,[5,6]].values
          y=all_df.iloc[:,[1]].values
          for a_tg_loc in all_tg_loc:
              for a_pass in all_target:
                  optics.PolynomialRegression(X, y, 2, variable, a_pass, a_tg_loc, fit_filename)

      #do the sieve_r reconstruction
      if fit_sieve_r_var == 1:
          variable = "sieve_r"
          X=all_df.iloc[:,[5,6]].values
          y=all_df.iloc[:,[9]].values
          for a_tg_loc in all_tg_loc:
              for a_pass in all_target:
                  optics.PolynomialRegression(X, y, 2, variable, a_pass, a_tg_loc, fit_filename)

      #do the phi reconstruction
      if fit_phi_var == 1:
          variable = "phi"
          X=all_df.iloc[:,[5,6,7,8]].values
          y=all_df.iloc[:,[2]].values
          for a_tg_loc in all_tg_loc:
              for a_pass in all_target:
                  optics.PolynomialRegression(X, y, 2, variable, a_pass, a_tg_loc, fit_filename)

      #do the momentum reconstruction
      if fit_momentum_var == 1:
          variable = "momentum"
          X=all_df.iloc[:,[5,6]].values
          y=all_df.iloc[:,[4]].values
          for a_tg_loc in all_tg_loc:
              for a_pass in all_target:
                  optics.PolynomialRegression(X, y, 3, variable, a_pass, a_tg_loc, fit_filename)

if __name__=='__main__':

    #define the input variables as the results from the ask_for_input() class
    main(1, 0, "p2", "Optics1", 0, 1, 0, 0, 0, "MagFieldStudy/Dipole3SameSC23/Dipole3SameSC23_Pass2_Optics1_sieveIN_elasticC12_1M_slim.root", "Dipole3SameSC23", 0, 4)

    ##def main(flag_csv_var, flag_fit_var, pass_value_var, tg_loc_var, flag_histo, fit_theta_var, fit_phi_var, fit_momentum_var, fit_sieve_r_var, filename_var, field_map_var, rot_angle, right_sector)
