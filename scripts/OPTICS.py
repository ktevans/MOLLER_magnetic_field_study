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

class OPTICS:

    def __init__(self):
        ##self.orig = pd.DataFrame()        # data before cut
        ##self.sec1 = pd.DataFrame()        # sector1 data before cut
        ##self.sec2 = pd.DataFrame()        # sector2 data before cut
        ##self.sec3 = pd.DataFrame()        # sector3 data before cut
        ##self.sec4 = pd.DataFrame()        # sector4 data before cut
        ##self.sec5 = pd.DataFrame()        # sector5 data before cut
        ##self.sec6 = pd.DataFrame()        # sector6 data before cut
        ##self.sec7 = pd.DataFrame()        # sector7 data before cut

        self.secNms = ['sec1', 'sec2', 'sec3', 'sec4', 'sec5', 'sec6', 'sec7']
        self.orig = pd.DataFrame()
        self.d = {}
        self.d = {name: pd.DataFrame for name in self.secNms}
        self.selected = pd.DataFrame()

        self.angle_lo=[]
        self.angle_up=[]

        ##use the following for non-rotation study
        ##for i in range(7):
            ##self.angle_lo.append(i*2*math.pi/7)# The entire phi region
            ##self.angle_up.append((i+1)*2*math.pi/7)


        ##self.selected = pd.DataFrame()    # data of selected holes

    def GenNumpyArray(self,filename):

        file = uproot.open(filename) #grab rootfile to analyze
        T=file["newT"] #define the tree from the root file

        geo = T.arrays(["gem1_x", "gem1_y","gem1_r","gem1_ph","gem1_px","gem1_py","gem1_pz","tg_th","tg_ph","tg_vz","tg_p","rate","sieve_r","sieve_ph"],library="pd")  # panda dictionary
        geo = geo.loc[geo["gem1_r"]>300] #filter the radial hits on the GEM to be above 300mm

        #geo["gem1_k"] = np.sqrt(geo.gem1_px*geo.gem1_px + geo.gem1_py*geo.gem1_py + geo.gem1_pz*geo.gem1_pz + 0.511*0.511)

        #print(geo["gem1_k"])
        #geo = geo.loc[abs(geo["gem1_k"] - 2200.0) < 2] ## cut for pass-1
        #geo = geo.loc[abs(geo["gem1_k"] - 4400.0) < 2] ## cut for pass-2
        #geo = geo.loc[abs(geo["gem1_k"] - 6600.0) < 2] ## cut for pass-3
        #geo = geo.loc[abs(geo["gem1_k"] - 8800.0) < 2] ## cut for pass-4

        #redifine phi to be from 0 to 2pi
        geo["tg_ph"] = [i+2*math.pi if i<0 else i for i in geo.tg_ph]
        geo["gem1_ph"] = [i+2*math.pi if i<0 else i for i in geo.gem1_ph]
        geo["sieve_ph"] = [i+2*math.pi if i<0 else i for i in geo.sieve_ph]

        self.orig=geo #the dataframe self.orig is the data from the root file

    def DefineSectors(self, rot_angle):
        rotation = 0.0

        if rot_angle==0:
            rotation = 0.0
        if rot_angle==51:
            rotation = 1*(2*math.pi/7)
        if rot_angle==102:
            rotation = 2*(2*math.pi/7)
        if rot_angle==154:
            rotation = 3*(2*math.pi/7)
        if rot_angle==205:
            rotation = 4*(2*math.pi/7)
        if rot_angle==257:
            rotation = 5*(2*math.pi/7)
        if rot_angle==308:
            rotation = 6*(2*math.pi/7)

        geo=self.orig

        #define the lower and upper azimuthal angle limits for each sector
        for i in range(7):
            self.angle_lo.append(i*2*math.pi/7 +rotation)
            self.angle_up.append((i+1)*2*math.pi/7 +rotation)
            ##angle_lo.append(i*2*math.pi/7)
            ##angle_up.append((i+1)*2*math.pi/7)
            self.d[self.secNms[i]] = geo.loc[(geo["gem1_ph"]<=self.angle_up[i])& (geo["gem1_ph"]>=self.angle_lo[i])]

        #print the angles for each sector
        ##print(angle_lo)
        ##print(angle_up)
        print("Sieve rotation: " + str(rot_angle) + " degrees")
        print("Sieve rotation: " + str(rotation) + " radians")

    def DrawHistAllSectors(self):
        fig, axs = plt.subplots(2, 4, figsize=(20,20))
        fig, bxs = plt.subplots(2, 4, figsize=(20,20))
        fig, cxs = plt.subplots(2, 4, figsize=(20,20))

        for i in range(2):
            for j in range(4):

                if i*4+j==7:
                    continue

                bxs[i,j].hist(self.d[self.secNms[i*4+j]].tg_th, 200)
                bxs[i,j].set_title(self.secNms[i*4+j])
                axs[i,j].hist2d(self.d[self.secNms[i*4+j]].gem1_r,self.d[self.secNms[i*4+j]].gem1_ph,(200,200),cmap=plt.cm.jet, cmin=1)
                axs[i,j].set_title(self.secNms[i*4+j])
                cxs[i,j].hist2d(self.d[self.secNms[i*4+j]].gem1_r,self.d[self.secNms[i*4+j]].tg_th,(200,200),cmap=plt.cm.jet, cmin=1)
                cxs[i,j].set_title(self.secNms[i*4+j])

        plt.show()

    def SelectOneHole(self, df):

        fig, ax = plt.subplots(figsize=(10,7))

        #plot gem1_r vs gem1_ph
        pts=ax.scatter(df.gem1_r,df.gem1_ph,s=5)

        #define variables that will be used to set axis limits and steps
        y_max=df.gem1_ph.max()
        y_min=df.gem1_ph.min()
        dy = (y_max-y_min)*0.1

        x_max=df.gem1_r.max()
        x_min=df.gem1_r.min()
        dx = (x_max-x_min)*0.1

        #set the axis limits
        ax.set_ylim(y_min-dy, y_max+dy)
        ax.set_xlim(x_min-dx, x_max+dx)

        #instigate hole selection module
        selector = SelectFromCollection(ax, pts)

##        print("Select points in the figure by enclosing them within a polygon.")
##        print("Press the 'esc' key to start a new polygon.")
##        print("Try holding the 'shift' key to move all of the vertices.")
##        print("Try holding the 'ctrl' key to move a single vertex.")

        plt.show()

        selector.disconnect()

        #fill the data frame with the selected points
        self.selected=df.loc[df.index[selector.ind]]

    def GenCSV(self, hole_id, filename):

        #the dataframe is from the selected data
        df=self.selected

        def local_phi_transformation(x):
            for i in range(7):
                if x > self.angle_lo[i] and x < self.angle_up[i]:
                    x = x - ((self.angle_lo[i]+self.angle_up[i])/2)
            return x

        #define dr/dz and dph/dz
        df["gem1_rp"] = (df.gem1_x*df.gem1_px+df.gem1_y*df.gem1_py)/(df.gem1_r*df.gem1_pz)
        df["gem1_php"] = (-df.gem1_y*df.gem1_px+df.gem1_x*df.gem1_py)/(df.gem1_r*df.gem1_pz)
        df["gem1_ph_local"] = df.gem1_ph.apply(local_phi_transformation)

        #define headers and write to csv
        header=["tg_th","tg_ph","tg_vz","tg_p","gem1_r","gem1_rp","gem1_ph","gem1_php","gem1_ph_local","sieve_r","sieve_ph","rate"]
        df.to_csv(filename,columns=header)

    def PolynomialRegression(self, X, y, degree, variable, fit_filename):

        #define training and test data
        X_train,X_test,y_train,y_test=train_test_split(X, y, test_size=0.33, random_state=42)

        #use the polynomial of the right degree
        poly = PolynomialFeatures(degree)
        X_train_new=poly.fit_transform(X_train)
        X_test_new=poly.fit_transform(X_test)

        #use a linear regression
        regression = linear_model.LinearRegression()
        model = regression.fit(X_train_new, y_train)
        y_pred = regression.predict(X_test_new)

        y_res = y_test-y_pred
        mean_res = np.mean(y_res)
        std_res = np.std(y_res)

        residual_sum_of_squares = y_res.T @ y_res #Q transpose Q
        N, p = X_test_new.shape

        sigma_squared_hat = residual_sum_of_squares[0,0]/(N-p)
        var = np.linalg.inv(X_test_new.T @ X_test_new)*sigma_squared_hat
        #for par in range(p):
            #standard_error = var[par,par]**0.5
            #print(standard_error)

        #define variables for the parameters and the score
        params = model.coef_
        intercept = model.intercept_
        score = model.score(X_test_new, y_test)

        #fill a text file with the parameters
        #fit_filename = "output/worstCase_asymmetric_optics"+tg_loc+"_"+pass_value+"_"+variable+"_parameters.txt"
        lines = [intercept, params, score]
        with open (fit_filename, 'w') as f:
            for line in lines:
                f.write(str(line))
                f.write('\n')

        print(intercept, params)
        print("score:  ", score)

        varNms = ["GEM r [mm]", "GEM rp", "GEM phi [rad]", "GEM phip"]

        #fig1, ax1 = plt.subplots(2,2)
        #fig1.canvas.manager.set_window_title(variable)

        #for i in range(1):
         #for j in range(2):

          #ax1[i,j].scatter(X_test[:,[i*2+j]],y_test, s=5, cmap='Greens')
          #ax1[i,j].scatter(X_test[:,[i*2+j]],y_pred, s=5, cmap='Reds')
          #ax1[i,j].set_ylabel(variable)
          #ax1[i,j].set_xlabel(varNms[i*2+j])

        if variable == "theta":
         fig, ax = plt.subplots(1,2)
         fig.canvas.manager.set_window_title(variable)
         ax[0].scatter(X_test[:,[0]],y_test[:,[0]], cmap='Greens', label="true")
         ax[0].scatter(X_test[:,[0]],y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[0].set_ylabel('target_theta (rad)')
         ax[0].set_xlabel('gem_r(mm)')
         ax[0].legend()
         ax[1].scatter( X_test[:,[1]], y_test[:,[0]], cmap='Greens', label="true")
         ax[1].scatter( X_test[:,[1]], y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[1].set_ylabel('target_theta(rad)')
         ax[1].set_xlabel('gem_rp')
         ax[1].legend()
         plt.show()

        if variable == "sieve_r":
         fig, ax = plt.subplots(1,2)
         fig.canvas.manager.set_window_title(variable)
         ax[0].scatter(X_test[:,[0]],y_test[:,[0]], cmap='Greens', label="true")
         ax[0].scatter(X_test[:,[0]],y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[0].set_ylabel('sieve_r (mm)')
         ax[0].set_xlabel('gem_r(mm)')
         ax[0].legend()
         ax[1].scatter( X_test[:,[1]], y_test[:,[0]], cmap='Greens', label="true")
         ax[1].scatter( X_test[:,[1]], y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[1].set_ylabel('sieve_r(mm)')
         ax[1].set_xlabel('gem_rp')
         ax[1].legend()
         plt.show()

        if variable == "phi":
         fig, ax = plt.subplots(2,2)
         fig.canvas.manager.set_window_title(variable)
         ax[0,0].scatter(X_test[:,[0]],y_test[:,[0]], cmap='Greens', label="true")
         ax[0,0].scatter(X_test[:,[0]],y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[0,0].set_ylabel('target_phi (rad)')
         ax[0,0].set_xlabel('gem_r(mm)')
         ax[0,0].legend()
         ax[0,1].scatter( X_test[:,[1]], y_test[:,[0]], cmap='Greens', label="true")
         ax[0,1].scatter( X_test[:,[1]], y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[0,1].set_ylabel('target_phi(rad)')
         ax[0,1].set_xlabel('gem_rp')
         ax[0,1].legend()
         ax[1,0].scatter(X_test[:,[2]],y_test[:,[0]], cmap='Greens', label="true")
         ax[1,0].scatter(X_test[:,[2]],y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[1,0].set_ylabel('target_phi (rad)')
         ax[1,0].set_xlabel('gem_phi')
         ax[1,0].legend()
         ax[1,1].scatter( X_test[:,[3]], y_test[:,[0]], cmap='Greens', label="true")
         ax[1,1].scatter( X_test[:,[3]], y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[1,1].set_ylabel('target_phi(rad)')
         ax[1,1].set_xlabel('gem_phip')
         ax[1,1].legend()
         plt.show()

        if variable == "momentum":
         fig, ax = plt.subplots(1,2)
         fig.canvas.manager.set_window_title(variable)
         ax[0].scatter(X_test[:,[0]],y_test[:,[0]], cmap='Greens', label="true")
         ax[0].scatter(X_test[:,[0]],y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[0].set_ylabel('target_z (mm)')
         ax[0].set_xlabel('gem_r(mm)')
         ax[0].legend()
         ax[1].scatter( X_test[:,[1]], y_test[:,[0]], cmap='Greens', label="true")
         ax[1].scatter( X_test[:,[1]], y_pred[:,[0]], cmap='Reds', label="predicted")
         ax[1].set_ylabel('target_z(mm)')
         ax[1].set_xlabel('gem_rp')
         ax[1].legend()
         plt.show()

        #plt.show()

        #c = ROOT.TCanvas()
        #hist = ROOT.TH1F("hist","Residual Distribution;Residuals(rad);Counts",150,-0.005,0.005)
        #f1 = ROOT.TF1("f1","gaus",-0.01,0.01,3)
        #for x in y_res:
        # hist.Fill(x)

        #f1.SetParameter(1,mean_res)
        #hist.Fit(f1)

        #for i in range(5):
        # hist.Fit(f1,"R","",f1.GetParameter(1)-1.5*f1.GetParameter(2), f1.GetParameter(1)+1.5*f1.GetParameter(2))

        #c.cd()
        #hist.Draw()
        #latex = ROOT.TLatex()
        #latex.DrawLatexNDC(0.2,0.8,"mean (mrad) = %f #pm %f"%(f1.GetParameter(1)*1e3, f1.GetParError(1)*1e3))
        #latex.DrawLatexNDC(0.2,0.7,"SD (mrad) = %f #pm %f"%(f1.GetParameter(2)*1e3, f1.GetParError(2)*1e3))
        #c.Draw()
        #c.Update()

def method():
  print("OPTICS")
