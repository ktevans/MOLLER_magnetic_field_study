################################################################################
##                               Kate Evans 2024                              ##
##   Script to perform basic aspects of the analysis for the magnetic field   ##
##                       study for the MOLLER experiment                      ##
##           Used confidence ellipse method from following reference:         ##
##  https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html  ##
################################################################################

## import modules
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.transforms as transforms
from matplotlib.backends.backend_pdf import PdfPages
import os
import configparser
import ast

config = configparser.ConfigParser()

class SieveHoleImageAnalysis:

    def __init__(self):

        self.prefix_list = []

        self.pass_num = ''
        self.target = ''
        self.rot_angle = ''
        self.holes = [13, 12, 11, 23, 22, 21, 33, 32, 31, 43, 42, 41, 53, 52, 51, 63, 62, 61, 73, 72, 71]

    def Gen_CSV_All(self, cfg_file):

        ## begining of path to each csv file
        path_sym = "output/Symmetric/"
        path_asym1 = "output/DipolePoint5RandSC23/"
        path_asym2 = "output/Dipole3SameSC23/"

        config.read(cfg_file)
        path_list = ast.literal_eval(config.get("Paths", "path_list"))

        pass_num = config['Simulation Settings']['pass_num']
        self.pass_num = pass_num
        target = config['Simulation Settings']['target']
        self.target = target
        rot_angle = config['Simulation Settings']['rot_angle']
        self.rot_angle = rot_angle

        ## middle of path to each csv file (same no matter what field map used)
        sub_path = "Pass" + pass_num + "_" + target + "/"

        prefix_list = []
        for p in path_list:
            if p == "output/Symmetric/":
                prefix_list.append(p + sub_path + "Symmetric_p" + pass_num + "_" + target + "_")
            if p == "output/DipolePoint5RandSC23/":
                prefix_list.append(p + sub_path + "DipolePoint5RandSC23_p" + pass_num + "_" + target + "_" + rot_angle + "degRot_")
            if p == "output/Dipole3SameSC23/":
                prefix_list.append(p + sub_path + "Dipole3SameSC23_p" + pass_num + "_" + target + "_" + rot_angle + "degRot_")
        self.prefix_list = prefix_list

        hole_numbers = self.holes

        ## csv file columns
        ## index, tg_th, tg_ph, tg_vz, tg_p, gem1_r, gem1_rp, gem1_ph, gem1_php, gem1_ph_local, sieve_r, sieve_ph, rate

        for p in prefix_list:
            for hole in hole_numbers:
                df = pd.read_csv(p + str(hole) + ".csv")
                df['hole_id'] = hole
                df.to_csv(p + str(hole) + ".csv")

        ## fill file lists
        for p in path_list:
            for filename in os.listdir(p + sub_path):
                begin_file = ''
                pref = ''
                files = []
                if p == "output/Symmetric/":
                    begin_file = "Symmetric_p" + pass_num + "_" + target + "_"
                    pref = prefix_list[0]
                if p == "output/DipolePoint5RandSC23/":
                    begin_file = "DipolePoint5RandSC23_p" + pass_num + "_" + target + "_" + rot_angle + "degRot_"
                    pref = prefix_list[1]
                if p == "output/Dipole3SameSC23/":
                    begin_file = "Dipole3SameSC23_p" + pass_num + "_" + target + "_" + rot_angle + "degRot_"
                    pref = prefix_list[2]
                for filename in os.listdir(p + sub_path):
                    if filename.startswith(begin_file) and filename.endswith(".csv") and not filename.endswith("_all.csv"):
                        files.append(filename)
                df_concat = pd.concat([pd.read_csv(p + sub_path + f) for f in files], ignore_index = True)
                df_concat.to_csv(pref + "all.csv")

    def MakeSinglePlots(self):

        file_prefix_sym = self.prefix_list[0]
        file_prefix_asym1 = self.prefix_list[1]
        file_prefix_asym2 = self.prefix_list[2]

        ## make list of different field maps
        field_maps = [file_prefix_sym, file_prefix_asym1, file_prefix_asym2]
        cols = ['hole_id', 'center_r', 'center_ph', 'eccentricity', 'r_err', 'ph_err', 'ecc_err']

        for field in field_maps:

            df_param = pd.DataFrame(columns = cols)
            dict_list = [] ## list that will track ellipse parameters

            with PdfPages(field + 'single_plots.pdf') as pdf:
                for h in self.holes:
                    df_hole = pd.read_csv(field + str(h) + ".csv")

                    fig, ax = plt.subplots(figsize=(6,6))
                    x = df_hole['gem1_r']
                    y = df_hole['gem1_ph']
                    ax.scatter(x, y)

                    ## find the covariance between the two datasets in order to calculate the Pearson correlation coefficient
                    cov = np.cov(x,y)
                    ## cov = [[(sigma_x)^2, simga_xy], [sigma_yx, (sigma_y)^2]]
                    ## cross terms of the covariance matrix give the correlation between x and y
                    ## p = sigma_xy / (sigma_x * signa_y)
                    pearson = cov[0,1]/np.sqrt(cov[0,0] * cov[1,1])

                    ## define correlation as positive or negative
                    corr = 0
                    if pearson > 0:
                        corr = 1
                    if pearson < 0:
                        corr = -1

                    ## using a special case to obtain the eigenvalues of this two-dimensional dataset
                    ell_radius_x = np.sqrt(1 + pearson)
                    ell_radius_y = np.sqrt(1 - pearson)

                    ellipse = Ellipse((0,0), width = ell_radius_x * 2, height = ell_radius_y * 2, facecolor = 'none', edgecolor = 'red')

                    ## calculating the standard deviation of x from the squareroot of the variance and multiplying with the given number of standard deviations
                    scale_x = np.sqrt(cov[0,0]) * 2.5
                    mean_x = np.mean(x)

                    ## calculating the standard deviation of y ...
                    scale_y = np.sqrt(cov[1, 1]) * 2.5
                    mean_y = np.mean(y)

                    ## transform the ellipse to surround the data
                    transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)
                    ellipse.set_transform(transf + ax.transData)

                    ## calculate the eccentricity of the ellipse as the slope of a line
                    std_x = np.std(x)
                    std_y = np.std(y)
                    slp = corr * ((std_y) / (std_x))

                    ## draw line through center with the slope equal to the eccentricity of the ellipse
                    ## caution: due to the skew of the data and the aspect ratio of the plot, the line can look like it does not pass through the ellipse center, so I have commented it out. But it's useful for understanding the results.
                    ## ax.axline((mean_x, mean_y), slope = slp, color = 'b', label = f'slope: {slp:0.5f} rad/mm')

                    n = 0
                    r_region = 2.5 * std_x
                    ph_region = 2.5 * std_y
                    for index, row in df_hole.iterrows():
                        if row['gem1_r'] < (mean_x + r_region) and row['gem1_r'] > (mean_x - r_region) and row['gem1_ph'] < (mean_y + ph_region) and row['gem1_ph'] > (mean_y - ph_region):
                            n += 1

                    cen = [mean_x, mean_y]
                    ellipse.set_label(f"center: [{mean_x:0.2f} mm, {mean_y:0.2f} rad] \n eccentricity: {slp:0.5f} rad/mm \n {n:0.0f} electrons")
                    ax.add_patch(ellipse)

                    ## calculate errors in the mean values
                    r_error = std_x / np.sqrt(n)
                    ph_error = std_y / np.sqrt(n)

                    ## calculate error in eccentricity
                    std_r_error = np.sqrt( (2 * np.power(std_x, 4)) / (n - 1))
                    std_ph_error = np.sqrt( (2 * np.power(std_y, 4)) / (n - 1))

                    ecc_err = np.absolute(slp * np.sqrt(np.power((std_r_error/std_x), 2) + np.power((std_ph_error/std_y), 2)))

                    ## record all the parameters from the ellipse and add to a list
                    row_dict = {'hole_id': h, 'center_r': cen[0], 'center_ph': cen[1], 'eccentricity': slp, 'r_err': r_error, 'ph_err': ph_error, 'ecc_err': ecc_err}
                    dict_list.append(row_dict)

                    ## format plot
                    ax.set_title('Hole ' + str(h) + ' image on the first GEM plane')
                    ax.set_xlabel("Radial position [mm]")
                    ax.set_ylabel("Azimuthal position [rad]")
                    ax.legend()

                    pdf.savefig()  ## saves the current figure into a pdf page
                    plt.close()

            df_param = pd.DataFrame.from_dict(dict_list)
            df_param.to_csv(field + 'ellipse_parameters.csv')

    def MakeComparisonPlots(self):

        file_prefix_sym = self.prefix_list[0]
        file_prefix_asym1 = self.prefix_list[1]
        file_prefix_asym2 = self.prefix_list[2]

        df_sym = pd.read_csv(file_prefix_sym + "ellipse_parameters.csv")
        x_sym = df_sym.index.values
        #cen_sym = df_sym['center_r']

        df_asym1 = pd.read_csv(file_prefix_asym1 + "ellipse_parameters.csv")
        x_asym1 = df_asym1.index.values
        #cen_asym1 = df_asym1['center_r']

        df_asym2 = pd.read_csv(file_prefix_asym2 + "ellipse_parameters.csv")
        x_asym2 = df_asym2.index.values
        #cen_asym2 = df_asym2['center_r']

        params = ['center_r', 'center_ph', 'eccentricity']

        for p in params:

            err = ''

            asym1_dif_col = df_sym[p] - df_asym1[p]
            asym2_dif_col = df_sym[p] - df_asym2[p]

            if p == 'center_r':
                err = 'r_err'
            if p == 'center_ph':
                err = 'ph_err'
            if p == 'eccentricity':
                err = 'ecc_err'

            fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8,8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

            df_compare = pd.DataFrame()
            df_compare = pd.concat([df_compare, df_sym['hole_id']], axis=1)
            df_compare = pd.concat([df_compare, asym1_dif_col.rename("sym_asym1_comp")], axis=1)
            df_compare = pd.concat([df_compare, asym2_dif_col.rename("sym_asym2_comp")], axis=1)

            ax.errorbar(x_sym, df_sym[p], yerr = df_sym[err], zorder=2, color = 'b', label = 'Symmetric Field Map', fmt = '.')
            ax.errorbar(x_asym1, df_asym1[p], yerr = df_asym1[err], zorder=3, color = 'r', label = 'DipolePoint5RandSC23 Field Map', fmt = '.')
            ax.errorbar(x_asym2, df_asym2[p], yerr = df_asym1[err], zorder=4, color = 'g', label = 'Dipole3SameSC23 Field Map', fmt = '.')

            ax2.plot(df_compare.index.values, df_compare['sym_asym1_comp'], color = 'r', label = 'Symmetric and DipolePoint5RandSC23', zorder=2)
            ax2.plot(df_compare.index.values, df_compare['sym_asym2_comp'], color = 'g', label = 'Symmetric and Dipole3SameSC23', zorder=3)

            labels = list(df_sym['hole_id'])
            ax2.xaxis.set_major_locator(ticker.FixedLocator(x_sym))
            ax2.xaxis.set_major_formatter(ticker.FixedFormatter(labels))

            ax.xaxis.grid(True, zorder=1)

            ax2.grid(True, zorder=1)

            var = ''
            axis = ''
            resid_label = ''

            if p == 'center_r':
                var = 'Radial Position of the Center'
                axis = 'Radial position [mm]'
                resid_label = 'Residual Values [mm]'
            if p == 'center_ph':
                var = 'Azimuthal Position of the Center'
                axis = 'Azimuthal position [rad]'
                resid_label = 'Residual Values [rad]'
            if p == 'eccentricity':
                var = 'Eccentricity of the Ellipse'
                axis = 'Eccentricity [rad/mm]'
                resid_label = 'Residual Values [rad/mm]'

            ax.set_title(var + ' of Sieve Hole Images on the First GEM Plane')
            ax2.set_xlabel("Sieve Hole ID")
            ax.set_ylabel(axis)
            ax.legend()

            ax2.set_ylabel(resid_label)
            ax2.legend()

            #plt.grid()
            plt.tight_layout()
            plt.savefig('output/Pass' + self.pass_num + '_' + self.target + '_' + p + '_Comparison.pdf')
            plt.close()
            #plt.show()

    def TestPlots(self):

        ## method for testing one plot at a time; used for code development

        file_prefix_sym = self.prefix_sym

        df = pd.DataFrame()

        df = pd.read_csv("output/Symmetric/Pass2_Optics1/Symmetric_p2_Optics1_13.csv")

        X = df['gem1_r']
        Y = df['gem1_ph']

if __name__=='__main__':

    imageAnalysis = SieveHoleImageAnalysis()

    imageAnalysis.Gen_CSV_All("scripts/config_files/template.ini")
    imageAnalysis.MakeSinglePlots()
    imageAnalysis.MakeComparisonPlots()

    #imageAnalysis.TestPlots()
