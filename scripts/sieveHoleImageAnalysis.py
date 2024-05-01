## import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
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

        self.holes = [13, 12, 11, 23, 22, 21, 33, 32, 31, 43, 42, 41, 53, 52, 51, 63, 62, 61, 73, 72, 71]

    def Gen_CSV_All(self):

        ## begining of path to each csv file
        path_sym = "output/Symmetric/"
        path_asym1 = "output/DipolePoint5RandSC23/"
        path_asym2 = "output/Dipole3SameSC23/"

        ## gather user input for energy pass, target, and rotation angle
        pass_num = input("What energy pass would you like to analyze?\n")
        target = input("Which target would you like to analyze?\n")
        rot_angle = input("How many degrees would you like the sieve to be rotated in azimuth? Options are 0, 51, 102, 154, 205, 257, 308\n")

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

        df_sym = self.sym
        df_asym1 = self.asym1
        df_asym2 = self.asym2

        file_prefix_sym = self.prefix_sym
        file_prefix_asym1 = self.prefix_asym1
        file_prefix_asym2 = self.prefix_asym2

        field_maps = [file_prefix_sym, file_prefix_asym1, file_prefix_asym2]

        for field in field_maps:
            with PdfPages(field + 'single_plots.pdf') as pdf:
                for h in self.holes:
                    df_hole = pd.read_csv(field + str(h) + ".csv")
                    fig, ax_nstd = plt.subplots(figsize=(6,6))
                    x = df_hole['gem1_r']
                    y = df_hole['gem1_ph']
                    ax_nstd.scatter(x, y)

                    cov = np.cov(x,y)
                    pearson = cov[0,1]/np.sqrt(cov[0,0] * cov[1,1])
                    #print(pearson)

                    #Using a special case to obtain the eigenvalues of this two-dimensional dataset.
                    ell_radius_x = np.sqrt(1 + pearson)
                    ell_radius_y = np.sqrt(1 - pearson)

                    ellipse_1 = Ellipse((0,0), width = ell_radius_x * 2, height = ell_radius_y * 2, facecolor = 'none', edgecolor = 'red', label = r'$1\sigma$')

                    ellipse_2 = Ellipse((0,0), width = ell_radius_x * 2, height = ell_radius_y * 2, facecolor = 'none', edgecolor = 'blue', label = r'$2\sigma$')

                    ellipse_3 = Ellipse((0,0), width = ell_radius_x * 2, height = ell_radius_y * 2, facecolor = 'none', edgecolor = 'green', label = r'$3\sigma$')

                    #Calculating the standard deviation of x from the squareroot of the variance and multiplying with the given number of standard deviations.
                    scale_x_1 = np.sqrt(cov[0,0]) * 1.0
                    scale_x_2 = np.sqrt(cov[0,0]) * 2.0
                    scale_x_3 = np.sqrt(cov[0,0]) * 3.0
                    mean_x = np.mean(x)

                    #Calculating the standard deviation of y ...
                    scale_y_1 = np.sqrt(cov[1, 1]) * 1.0
                    scale_y_2 = np.sqrt(cov[1, 1]) * 2.0
                    scale_y_3 = np.sqrt(cov[1, 1]) * 3.0
                    mean_y = np.mean(y)

                    transf1 = transforms.Affine2D().rotate_deg(45).scale(scale_x_1, scale_y_1).translate(mean_x, mean_y)
                    transf2 = transforms.Affine2D().rotate_deg(45).scale(scale_x_2, scale_y_2).translate(mean_x, mean_y)
                    transf3 = transforms.Affine2D().rotate_deg(45).scale(scale_x_3, scale_y_3).translate(mean_x, mean_y)

                    ellipse_1.set_transform(transf1 + ax_nstd.transData)
                    ax_nstd.add_patch(ellipse_1)
                    ellipse_2.set_transform(transf2 + ax_nstd.transData)
                    ax_nstd.add_patch(ellipse_2)
                    ellipse_3.set_transform(transf3 + ax_nstd.transData)
                    ax_nstd.add_patch(ellipse_3)

                    ax_nstd.set_title('Hole ' + str(h) + ' image on the first GEM plane')
                    ax_nstd.set_xlabel("Radial position [mm]")
                    ax_nstd.set_ylabel("Azimuthal position [rad]")
                    ax_nstd.legend()

                    pdf.savefig()  # saves the current figure into a pdf page
                    plt.close()

    def TestPlots(self):

        file_prefix_sym = self.prefix_sym
        file_prefix_asym1 = self.prefix_asym1
        file_prefix_asym2 = self.prefix_asym2

        df_hole = pd.read_csv(file_prefix_sym  + "12.csv")
        fig, ax = plt.subplots(figsize=(6,6))
        x = df_hole['gem1_r']
        y = df_hole['gem1_ph']
        ax.scatter(x, y)

        n_std = 3.0
        cov = np.cov(x,y)
        pearson = cov[0,1]/np.sqrt(cov[0,0] * cov[1,1])
        #print(pearson)

        #Using a special case to obtain the eigenvalues of this two-dimensional dataset.
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)

        ellipse = Ellipse((0,0), width = ell_radius_x * 2, height = ell_radius_y * 2, facecolor = 'none', edgecolor='red')

        #Calculating the standard deviation of x from the squareroot of the variance and multiplying with the given number of standard deviations.
        scale_x = np.sqrt(cov[0,0]) * n_std
        mean_x = np.mean(x)

        #Calculating the standard deviation of y ...
        scale_y = np.sqrt(cov[1, 1]) * n_std
        mean_y = np.mean(y)

        transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)

        ellipse.set_transform(transf + ax.transData)
        ax.add_patch(ellipse)

        ax.set_title('Hole 12 image on the first GEM plane')
        ax.set_xlabel("Radial position [mm]")
        ax.set_ylabel("Azimuthal position [rad]")

        plt.show()

        #pdf.savefig()  # saves the current figure into a pdf page
        #plt.close()

if __name__=='__main__':

    imageAnalysis = SieveHoleImageAnalysis()

    imageAnalysis.Gen_CSV_All()
    imageAnalysis.MakeSinglePlots()

    #imageAnalysis.TestPlots()
