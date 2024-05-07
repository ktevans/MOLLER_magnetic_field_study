## import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.transforms as transforms
from matplotlib.backends.backend_pdf import PdfPages
import os

class SieveHoleImageAnalysis:

    def __init__(self):

        ## construct data frames that will be used later
        self.sym = pd.DataFrame()
        self.asym1 = pd.DataFrame()
        self.asym2 = pd.DataFrame()

        self.prefix_sym = ""
        self.prefix_asym1 = ""
        self.prefix_asym2 = ""

        self.pass_num = ''
        self.target = ''
        self.rot_angle = ''
        self.holes = [13, 12, 11, 23, 22, 21, 33, 32, 31, 43, 42, 41, 53, 52, 51, 63, 62, 61, 73, 72, 71]

    def Gen_CSV_All(self):

        ## begining of path to each csv file
        path_sym = "output/Symmetric/"
        path_asym1 = "output/DipolePoint5RandSC23/"
        path_asym2 = "output/Dipole3SameSC23/"

        ## gather user input for energy pass, target, and rotation angle
        pass_num = input("What energy pass would you like to analyze?\n")
        self.pass_num = pass_num
        target = input("Which target would you like to analyze?\n")
        self.target = target
        rot_angle = input("How many degrees would you like the sieve to be rotated in azimuth? Options are 0, 51, 102, 154, 205, 257, 308\n")
        self.rot_angle = rot_angle

        ## middle of path to each csv file (same no matter what field map used)
        sub_path = "Pass" + pass_num + "_" + target + "/"

        ## file name excluding hole id number and .csv
        file_prefix_sym = path_sym + sub_path + "Symmetric_p" + pass_num + "_" + target + "_"
        #print(file_prefix_sym)
        file_prefix_asym1 = path_asym1 + sub_path + "DipolePoint5RandSC23_p" + pass_num + "_" + target + "_" + rot_angle + "degRot_"
        #print(file_prefix_asym1)
        file_prefix_asym2 = path_asym2 + sub_path + "Dipole3SameSC23_p" + pass_num + "_" + target + "_" + rot_angle + "degRot_"
        #print(file_prefix_asym2)

        self.prefix_sym = file_prefix_sym
        self.prefix_asym1 = file_prefix_asym1
        self.prefix_asym2 = file_prefix_asym2

        hole_numbers = self.holes

        ## csv file columns
        ## index, tg_th, tg_ph, tg_vz, tg_p, gem1_r, gem1_rp, gem1_ph, gem1_php, gem1_ph_local, sieve_r, sieve_ph, rate

        for hole in hole_numbers:
            ## read each csv file and add a column that lists the hole id number

            df_sym = pd.read_csv(file_prefix_sym + str(hole) + ".csv")
            df_sym['hole_id'] = hole
            df_sym.to_csv(file_prefix_sym + str(hole) + ".csv")

            df_asym1 = pd.read_csv(file_prefix_asym1 + str(hole) + ".csv")
            df_asym1['hole_id'] = hole
            df_asym1.to_csv(file_prefix_asym1 + str(hole) + ".csv")

            df_asym2 = pd.read_csv(file_prefix_asym2 + str(hole) + ".csv")
            df_asym2['hole_id'] = hole
            df_asym2.to_csv(file_prefix_asym2 + str(hole) + ".csv")

        ## csv file columns
        ## index, tg_th, tg_ph, tg_vz, tg_p, gem1_r, gem1_rp, gem1_ph, gem1_php, gem1_ph_local, sieve_r, sieve_ph, rate, hole_id

        ## list of files that should be combined into one CSV file, currently empty but will be filled
        files_sym = []
        files_asym1 = []
        files_asym2 = []

        ## fill file lists
        for filename in os.listdir(path_sym + sub_path):
            if filename.startswith("Symmetric_p" + pass_num + "_" + target + "_") and filename.endswith(".csv") and not filename.endswith("_all.csv"):
                files_sym.append(filename)
        for filename in os.listdir(path_asym1 + sub_path):
            if filename.startswith("DipolePoint5RandSC23_p" + pass_num + "_" + target + "_" + rot_angle + "degRot_") and filename.endswith(".csv") and not filename.endswith("_all.csv"):
                files_asym1.append(filename)
        for filename in os.listdir(path_asym2 + sub_path):
            if filename.startswith("Dipole3SameSC23_p" + pass_num + "_" + target + "_" + rot_angle + "degRot_") and filename.endswith(".csv") and not filename.endswith("_all.csv"):
                files_asym2.append(filename)

        #for f in files_sym:
            #print(path_sym + sub_path + f + "\n")

        ## add together all the CSV files for a specific configuration and specific field map

        df_concat_sym = pd.concat([pd.read_csv(path_sym + sub_path + f) for f in files_sym], ignore_index = True)
        df_concat_sym.to_csv(file_prefix_sym + "all.csv")

        df_concat_asym1 = pd.concat([pd.read_csv(path_asym1 + sub_path + f) for f in files_asym1], ignore_index = True)
        df_concat_asym1.to_csv(file_prefix_asym1 + "all.csv")

        df_concat_asym2 = pd.concat([pd.read_csv(path_asym2 + sub_path + f) for f in files_asym2], ignore_index = True)
        df_concat_asym2.to_csv(file_prefix_asym2 + "all.csv")

        self.sym = df_concat_sym
        self.asym1 = df_concat_asym1
        self.asym2 = df_concat_asym2

    def MakeSinglePlots(self):

        file_prefix_sym = self.prefix_sym
        file_prefix_asym1 = self.prefix_asym1
        file_prefix_asym2 = self.prefix_asym2

        field_maps = [file_prefix_sym, file_prefix_asym1, file_prefix_asym2]
        cols = ['hole_id', 'center_r', 'center_ph', 'eccentricity']

        for field in field_maps:

            df_param = pd.DataFrame(columns = cols)
            dict_list = []

            with PdfPages(field + 'single_plots.pdf') as pdf:
                for h in self.holes:
                    df_hole = pd.read_csv(field + str(h) + ".csv")

                    fig, ax = plt.subplots(figsize=(6,6))
                    x = df_hole['gem1_r']
                    y = df_hole['gem1_ph']
                    ax.scatter(x, y)

                    #Find the covariance between the two datasets in order to calculate the Pearson correlation coefficient
                    cov = np.cov(x,y)
                    # p = cov[x,y] / sqrt(sigma_x * signa_y)
                    pearson = cov[0,1]/np.sqrt(cov[0,0] * cov[1,1])

                    #Define if correlation is positive or negative
                    corr = 0
                    if pearson > 0:
                        corr = 1
                    if pearson < 0:
                        corr = -1

                    #Using a special case to obtain the eigenvalues of this two-dimensional dataset.
                    ell_radius_x = np.sqrt(1 + pearson)
                    ell_radius_y = np.sqrt(1 - pearson)

                    ellipse = Ellipse((0,0), width = ell_radius_x * 2, height = ell_radius_y * 2, facecolor = 'none', edgecolor = 'red')

                    #Calculating the standard deviation of x from the squareroot of the variance and multiplying with the given number of standard deviations.
                    scale_x = np.sqrt(cov[0,0]) * 2.5
                    mean_x = np.mean(x)

                    #Calculating the standard deviation of y ...
                    scale_y = np.sqrt(cov[1, 1]) * 2.5
                    mean_y = np.mean(y)

                    #Transform the ellipse to surround the data
                    transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)

                    ellipse.set_transform(transf + ax.transData)

                    #Calculate the eccentricity of the ellipse as the slope of a line
                    std_x = np.std(x)
                    std_y = np.std(y)
                    slp = corr * (std_y) / (std_x)

                    ax.axline((mean_x, mean_y), slope = slp, color = 'b', label = f'slope: {slp:0.5f}')

                    cen = [mean_x, mean_y]
                    ellipse.set_label(f"center: [{mean_x:0.2f}, {mean_y:0.2f}]")
                    ax.add_patch(ellipse)

                    #record all the parameters from the ellipse and add to a list
                    row_dict = {'hole_id': h, 'center_r': cen[0], 'center_ph': cen[1], 'eccentricity': slp}
                    dict_list.append(row_dict)

                    ax.set_title('Hole ' + str(h) + ' image on the first GEM plane')
                    ax.set_xlabel("Radial position [mm]")
                    ax.set_ylabel("Azimuthal position [rad]")
                    ax.legend()

                    pdf.savefig()  # saves the current figure into a pdf page
                    plt.close()

            df_param = pd.DataFrame.from_dict(dict_list)
            df_param.to_csv(field + 'ellipse_parameters.csv')

    def MakeComparisonPlots(self):

        file_prefix_sym = self.prefix_sym
        file_prefix_asym1 = self.prefix_asym1
        file_prefix_asym2 = self.prefix_asym2

        #field_maps = [file_prefix_sym, file_prefix_asym1, file_prefix_asym2]

        #fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8,8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

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

            asym1_dif_col = df_sym[p] - df_asym1[p]
            asym2_dif_col = df_sym[p] - df_asym2[p]

            fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8,8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

            df_compare = pd.DataFrame()
            df_compare = pd.concat([df_compare, df_sym['hole_id']], axis=1)
            df_compare = pd.concat([df_compare, asym1_dif_col.rename("sym_asym1_comp")], axis=1)
            df_compare = pd.concat([df_compare, asym2_dif_col.rename("sym_asym2_comp")], axis=1)

            ax.scatter(x_sym, df_sym[p], zorder=2, color = 'b', label = 'Symmetric Field Map', s=10)
            ax.scatter(x_asym1, df_asym1[p], zorder=3, color = 'r', label = 'DipolePoint5RandSC23 Field Map', s=10)
            ax.scatter(x_asym2, df_asym2[p], zorder=4, color = 'g', label = 'Dipole3SameSC23 Field Map', s=10)

            ax2.plot(df_compare.index.values, df_compare['sym_asym1_comp'], color = 'r', label = 'Symmetric and DipolePoint5RandSC23', zorder=2)
            ax2.plot(df_compare.index.values, df_compare['sym_asym2_comp'], color = 'g', label = 'Symmetric and Dipole3SameSC23', zorder=3)

            labels = list(df_sym['hole_id'])
            ax2.xaxis.set_major_locator(ticker.FixedLocator(x_sym))
            ax2.xaxis.set_major_formatter(ticker.FixedFormatter(labels))

            ax.xaxis.grid(True, zorder=1)

            ax2.grid(True, zorder=1)

            var = ''
            axis = ''

            if p == 'center_r':
                var = 'Radial Position of the Center'
                axis = 'Radial position [mm]'
            if p == 'center_ph':
                var = 'Azimuthal Position of the Center'
                axis = 'Azimuthal position [rad]'
            if p == 'eccentricity':
                var = 'Eccentricity of the Ellipse'
                axis = 'Eccentricity [rad/mm]'

            ax.set_title(var + ' of Sieve Hole Images on the First GEM Plane')
            ax2.set_xlabel("Sieve Hole ID")
            ax.set_ylabel(axis)
            ax.legend()

            ax2.set_ylabel("Residual Values")
            ax2.legend()

            #plt.grid()
            plt.tight_layout()
            plt.savefig('output/Pass' + self.pass_num + '_' + self.target + '_' + p + '_Comparison.pdf')
            plt.close()
            #plt.show()

    def TestPlots(self):

        file_prefix_sym = self.prefix_sym

        df = pd.DataFrame()

        df = pd.read_csv("output/Symmetric/Pass2_Optics1/Symmetric_p2_Optics1_13.csv")

        nstd = 2.5

        mean_r = df.loc[:, 'gem1_r'].mean()
        mean_ph = df.loc[:, 'gem1_ph'].mean()

        std_r = df.loc[:, 'gem1_r'].std()
        std_ph = df.loc[:, 'gem1_ph'].std()

        ellipse = Ellipse((mean_r, mean_ph), width = std_r * nstd, height = std_ph * nstd * 2, facecolor = 'none', edgecolor = 'red', label = 'ellipse')

        fig, ax = plt.subplots(figsize=(6,6))
        ax.scatter(df['gem1_r'], df['gem1_ph'])

        ax.add_patch(ellipse)
        ax.legend()

        plt.show()

if __name__=='__main__':

    imageAnalysis = SieveHoleImageAnalysis()

    imageAnalysis.Gen_CSV_All()
    imageAnalysis.MakeSinglePlots()
    imageAnalysis.MakeComparisonPlots()

    #imageAnalysis.TestPlots()
