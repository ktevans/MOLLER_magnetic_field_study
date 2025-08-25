import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.transforms as transforms
from matplotlib.backends.backend_pdf import PdfPages
from Find_Files import FindFiles
from DrawElipse import DrawElipse, MakeElipseMap, MakeScatter, MakeMeans, GrabValues, DrawAnyElipse, GrabAnyValues
from OneDPlot import OneDGraph
from scipy.optimize import curve_fit

#This code makes three plots: Scatter, Ellipse, and Means and helps understand how the values change as the magnetic coils are offset
def CompareOffsets(Hole = '', Pass = '', Optics = '', xvalue = '', yvalue = '', SecRot = '', Type = ''):
    if 'Even' in Type:
        types = ['in2mm', 'Symmetric', 'out2mm', 'out4mm']
        colors = ['#ff0000', '#cccc00', '#258e8e', '#730099']
        offset = [-2, 0, 2, 4]
    else:
        types = ['in2mm', 'in1mm', 'Symmetric', 'out1mm', 'out2mm', 'out3mm', 'out4mm']
        colors = ['#ff0000', '#ff8000', '#cccc00', 'green', '#258e8e', 'blue', '#730099']
        offset = [-2, -1, 0, 1, 2, 3, 4]
        print('Unknown Input for Type, please use: Normal or Even')
    #Mapping is used to define the axis for plots
    mapping = {
    'gem_r': 'GEM radial position (mm)',
    'gem_ph': 'GEM azimuthal position (rad)',
    'r_prime': 'GEM radial position wrt z',
    'phi_prime': 'GEM azimuthal position wrt z'
    }
    xvaluen = mapping.get(xvalue, xvalue)
    yvaluen = mapping.get(yvalue, yvalue)
    fig, ax = plt.subplots()
    for type, color in zip(types, colors):
        #This filepath code is common and is how filepaths are made
        #Remember! This code needs specific phrases to work, look in Find_Files.py for more information on specifics
        file_path = FindFiles(type + '' + Pass + '' + Optics + SecRot) + Hole + '.csv'
        MakeScatter(F1=file_path, xaxis=xvalue, yaxis=yvalue, color=color, ax=ax, label = type)
    ax.set_xlabel(xvaluen)
    ax.set_ylabel(yvaluen)
    ax.set_title(Pass + ' ' + Optics + ' Hole ' + Hole + ' ' + yvalue + ' by ' + xvalue + ' graph')
    ax.legend(title="Offset")
    plt.show()
    MakeElipseMap(Hole = Hole, Pass = Pass, Optics = Optics, xvalue = xvalue, yvalue = yvalue, Type = Type, SecRotE = SecRot)
    fig, ax = plt.subplots()
    for type, color in zip(types, colors):
        file_path = FindFiles(type + '' + Pass + '' + Optics + SecRot) + Hole + '.csv'
        MakeMeans(F1=file_path, xaxis=xvalue, yaxis=yvalue, color=color, ax=ax, label = type)
    ax.set_xlabel(xvaluen)
    ax.set_ylabel(yvaluen)
    ax.set_title(Pass + ' ' + Optics + ' Hole ' + Hole + ' ' + yvalue + ' by ' + xvalue + ' graph')
    ax.legend(title="Offset")
    plt.show()

#Takes holes at a set offset and compares the difference in optics through ellipses
#Looks complicated but is fairly simple with methods defined earlier
def CompareOptics(Hole = '', Pass = '',Displacment = '', xvalue = '', yvalue = ''):
    Optics = ['Optics1', 'Optics2', 'Optics3']
    colors = ['#ff0000', 'green', 'blue']
    xmeans, ymeans, xerrs, yerrs, LowX_Values, HighX_Values, LowY_Values, HighY_Values = ([] for _ in range(8))
    fig, ax = plt.subplots()
    for optic, color in zip(Optics, colors):
        file_path = FindFiles(Displacment + Pass + optic) + Hole + '.csv'
        ax, LowX, HighX, LowY, HighY = DrawElipse(F1=file_path, xaxis=xvalue, yaxis=yvalue, color=color, ax=ax, label=optic)
        xmean, ymean, xerr, yerr, Focalx, Focaly = GrabValues(F1 = file_path, xaxis = xvalue, yaxis = yvalue)
        LowX_Values.append(LowX)
        HighX_Values.append(HighX)
        LowY_Values.append(LowY)
        HighY_Values.append(HighY)
        ymeans.append(ymean)
        xmeans.append(xmean)
        xerrs.append(xerr)
        yerrs.append(yerr)
    print(abs(xmeans[0] - xmeans[1]), xerrs[0] + xerrs[1], abs(xmeans[0] - xmeans[2]), xerrs[0] + xerrs[2], abs(xmeans[1] - xmeans[2]), xerrs[1] + xerrs[2])
    print(abs(ymeans[0] - ymeans[1]), yerrs[0] + yerrs[1], abs(ymeans[0] - ymeans[2]), yerrs[0] + yerrs[2], abs(ymeans[1] - ymeans[2]), yerrs[1] + yerrs[2])
    ax.set_xlim(min(LowX_Values), max(HighX_Values))
    ax.set_ylim(min(LowY_Values), max(HighY_Values))
    ax.set_title(Pass + ' Hole ' + Hole + ' Offset ' + Displacment + ' ' + yvalue + ' by ' + xvalue)
    mapping = {
    'gem_r': 'GEM radial position (mm)',
    'gem_ph': 'GEM azimuthal position (rad)',
    'r_prime': 'GEM radial position wrt z',
    'phi_prime': 'GEM azimuthal position wrt z'
    }
    xvalue = mapping.get(xvalue, xvalue)
    yvalue = mapping.get(yvalue, yvalue)
    ax.set_xlabel(xvalue)
    ax.set_ylabel(yvalue)
    ax.legend(title="Offset")
    plt.show()

#Simply translates the values into cartesin for X and Y plots
def TranslateToCart(phivals = [], rvals = []):
    xvals = []
    yvals = []
    for phi, r in zip(phivals, rvals):
        yval = (r * (math.sin(phi)))
        xval = (r * (math.cos(phi)))
        xvals.append(xval)
        yvals.append(yval)
    return(xvals, yvals)

#Defines a linear function for fitting
def linear(x, m, b):
    return m * x + b

#This code will take the means of the defined xvalues and yvalues and plots them against changing offset
#This trend is expected to be somewhat linear so a linear fit is added
#Rudimentary uncertainty is also used (Though it is very basic and will need some work)
def QuantifyChangingOffsets(Hole = '', Pass = '', Optics = '', xvalue = '', yvalue = '',SecRot = '', Type = ''):
    if 'Even' in Type:
        types = ['in2mm', 'Symmetric', 'out2mm', 'out4mm']
        colors = ['#ff0000', '#cccc00', '#258e8e', '#730099']
        offset = [-2, 0, 2, 4]
    else:
        types = ['in2mm', 'in1mm', 'Symmetric', 'out1mm', 'out2mm', 'out3mm', 'out4mm']
        colors = ['#ff0000', '#ff8000', '#cccc00', 'green', '#258e8e', 'blue', '#730099']
        offset = [-2, -1, 0, 1, 2, 3, 4]
    ymeans, xmeans, xerrs, yerrs = [], [], [], []
    for type, color in zip(types, colors):
        file_path = FindFiles(type + '' + Pass + '' + Optics + SecRot) + Hole + '.csv'
        xmean, ymean, xerr, yerr, Focalx, Focaly = GrabValues(F1=file_path, xaxis=xvalue, yaxis=yvalue)
        ymeans.append(ymean)
        xmeans.append(xmean)
        xerrs.append(xerr)
        yerrs.append(yerr)
    print(yerrs)
    #We want to see how the values varry from symmetric so we center all values around symmetric and make symmetric zero, this is what the code below does and this is done multiple times throughout
    symmetricvalueym = ymeans[2]
    symmetricvaluexm = xmeans[2]
    ymeans = [x - symmetricvalueym for x in ymeans]
    xmeans = [x - symmetricvaluexm for x in xmeans]
    mapping = {
    'gem_r': 'Δ GEM radial position from Symmetric (mm)',
    'gem_ph': 'Δ GEM azimuthal position from Symmetric (rad)',
    'r_prime': 'Δ GEM radial position wrt z from Symmetric',
    'phi_prime': 'Δ GEM azimuthal position wrt z from Symmetric'
    }
    xvalue = mapping.get(xvalue, xvalue)
    yvalue = mapping.get(yvalue, yvalue)
    #Fitline makes the fitted linear line with error
    coeffs_y = np.polyfit(offset, ymeans, 1)
    fitline_y = np.poly1d(coeffs_y)
    popt_y, pcov_y = curve_fit(linear, offset, ymeans, sigma=yerrs, absolute_sigma=True)
    slope_y, intercept_y = popt_y
    slope_err_y = np.sqrt(np.diag(pcov_y))[0]  # Uncertainty in the slope
    fitline_y = linear(np.array(offset), slope_y, intercept_y)
    plt.plot(offset, fitline_y, label=f'Slope = {slope_y:.5f} ± {slope_err_y:.5f}', linestyle='--', color='black')
    plt.legend()
    plt.errorbar(offset, ymeans, yerr = yerrs, fmt='o')
    plt.xlabel('Magnetic Offset (mm)')
    plt.ylabel(yvalue + ' means')
    plt.title('1D Plot for Hole ' + Hole + ' ' + Pass + ' ' + Optics + ' ' + SecRot)
    plt.show()

    popt_x, pcov_x = curve_fit(linear, offset, xmeans, sigma=xerrs, absolute_sigma=True)
    slope_x, intercept_x = popt_x
    slope_err_x = np.sqrt(np.diag(pcov_x))[0]
    fitline_x = linear(np.array(offset), slope_x, intercept_x)
    plt.plot(offset, fitline_x, label=f'Slope = {slope_x:.5f} ± {slope_err_x:.5f}', linestyle='--', color='black')
    plt.legend()
    plt.errorbar(offset, xmeans, yerr = xerrs, fmt='o')
    plt.xlabel('Magnetic Offset (mm)')
    plt.ylabel(xvalue + ' means')
    plt.title('1D Plot for Hole ' + Hole + ' ' + Pass + ' ' + Optics + ' ' + SecRot)
    plt.show()

#This does the same as the code above but uses cartesian coordinates instead
#Due to cartesin coordinates being used it also calulates ellipse angle and eccentricity computed in the same way touched on further in the thesis
#Notice no xvalue or yvalue are defined, this is because you are computing X and Y so gem_r and gem_ph are automatically going to be used
def XandYplots(Hole = '', Pass = '', Optics = '',SecRot = '', Type = ''):
    if 'Even' in Type:
        types = ['in2mm', 'Symmetric', 'out2mm', 'out4mm']
        colors = ['#ff0000', '#cccc00', '#258e8e', '#730099']
        offset = [-2, 0, 2, 4]
    else:
        types = ['in2mm', 'in1mm', 'Symmetric', 'out1mm', 'out2mm', 'out3mm', 'out4mm']
        colors = ['#ff0000', '#ff8000', '#cccc00', 'green', '#258e8e', 'blue', '#730099']
        offset = [-2, -1, 0, 1, 2, 3, 4]
        print('Unknown Input for Type, please use: Normal or Even')
    xvalued = 'gem_r'
    yvalued = 'gem_ph'
    Xmeans, Ymeans, Focalxs, Focalys, Angles, xerrs, yerrs = ([] for _ in range(7))
    fig, ax = plt.subplots()
    for type, color in zip(types, colors):
        F1 = FindFiles(type + '' + Pass + '' + Optics + SecRot) + Hole + '.csv'
        df = pd.read_csv(F1)
        df[xvalued] = pd.to_numeric(df[xvalued], errors='coerce')
        df[yvalued] = pd.to_numeric(df[yvalued], errors='coerce')
        df = df.dropna(subset=[xvalued, yvalued])
        rvalues = df[xvalued].dropna().tolist()
        phvalues = df[yvalued].dropna().tolist()
        valueX = []
        valueY = []
        for r, phi, in zip(rvalues, phvalues):
            xvalue = float(r) * math.cos(float(phi))
            yvalue = float(r) * math.sin(float(phi))
            valueX.append(int(xvalue))
            valueY.append(int(yvalue))
        DrawAnyElipse(xvalues = valueX, yvalues = valueY, color = color, ax=ax, label = type)
        xmean, ymean, Focalx, Focaly, theta = GrabAnyValues(xvalues = valueX, yvalues = valueY)
        xerr = np.std(valueX) / (np.sqrt(len(valueX)))
        yerr = np.std(valueY)/ (np.sqrt(len(valueY)))
        xerrs.append(xerr)
        yerrs.append(yerr)
        Angles.append(theta)
        Ymeans.append(ymean)
        Xmeans.append(xmean)
        Focalxs.append(Focaly)
        Focalys.append(Focalx)
    symmetricvalueym = Ymeans[2]
    symmetricvaluexm = Xmeans[2]
    Ymeans = [x - symmetricvalueym for x in Ymeans]
    Xmeans = [x - symmetricvaluexm for x in Xmeans]
    Eccentricity = []
    for Focalx, Focaly in zip(Focalxs, Focalys):
        AFocalx = abs(Focalx[0] - Focalx[1])
        AFocaly = abs(Focaly[0] - Focaly[1])
        FocalDist = np.sqrt((np.square(AFocalx) + np.square(AFocaly)))
        Angle = np.arctan((AFocaly) / (AFocalx))
        Eccentricity.append(FocalDist)
    symmetricEccentricity = Eccentricity[2]
    Eccentricity = [x - symmetricEccentricity for x in Eccentricity]
    symmetricAngle = Angles[2]
    Angles = [x - symmetricAngle for x in Angles]
    mapping = {
    'gem_r': 'Δ GEM radial position from Symmetric (mm)',
    'gem_ph': 'Δ GEM azimuthal position from Symmetric (rad)',
    'r_prime': 'Δ GEM radial position wrt z from Symmetric',
    'ph_prime': 'Δ GEM azimuthal position wrt z from Symmetric'
    }
    xvalue = mapping.get(xvalue, xvalue)
    yvalue = mapping.get(yvalue, yvalue)
    plt.scatter(offset, Xmeans)

    plt.xlabel('offset (mm)')
    plt.ylabel('x value means (mm)')
    plt.title('1D Plot for Hole ' + Hole + ' ' + Pass + ' ' + Optics + ' ' + SecRot)
    plt.show()

    coeffs_y = np.polyfit(offset, Ymeans, 1)
    fitline_y = np.poly1d(coeffs_y)
    popt_y, pcov_y = curve_fit(linear, offset, Ymeans, sigma=yerrs, absolute_sigma=True)
    slope_y, intercept_y = popt_y
    slope_err_y = np.sqrt(np.diag(pcov_y))[0]
    fitline_y = linear(np.array(offset), slope_y, intercept_y)
    plt.plot(offset, fitline_y, label=f'Slope = {slope_y:.5f} ± {slope_err_y:.5f}', linestyle='--', color='black')
    plt.errorbar(offset, Ymeans, yerr = yerrs, fmt='o')
    plt.legend()
    plt.xlabel('offset (mm)')
    plt.ylabel('y value means (mm)')
    plt.title('1D Plot for Hole ' + Hole + ' ' + Pass + ' ' + Optics + ' ' + SecRot)
    plt.show()

    popt_x, pcov_x = curve_fit(linear, offset, Xmeans, sigma=xerrs, absolute_sigma=True)
    slope_x, intercept_x = popt_x
    slope_err_x = np.sqrt(np.diag(pcov_x))[0]
    fitline_x = linear(np.array(offset), slope_x, intercept_x)
    plt.plot(offset, fitline_x, label=f'Slope = {slope_x:.5f} ± {slope_err_x:.5f}', linestyle='--', color='black')
    plt.errorbar(offset, Xmeans, yerr = xerrs, fmt='o')
    plt.legend()
    plt.xlabel('offset (mm)')
    plt.ylabel('x value means (mm)')
    plt.title('1D Plot for Hole ' + Hole + ' ' + Pass + ' ' + Optics + ' ' + SecRot)
    plt.show()

    plt.scatter(offset, Eccentricity)
    plt.xlabel('offset (mm)')
    plt.ylabel('Δ Relative Eccentricity from Symmetric (mm)')
    plt.title('1D Plot for Hole ' + Hole + ' ' + Pass + ' ' + Optics + ' ' + SecRot)
    plt.show()

    popt_a, pcov_a = curve_fit(linear, offset, Angles)
    slope_a, intercept_a = popt_a
    fitline_a = linear(np.array(offset), slope_a, intercept_a)
    plt.plot(offset, fitline_a, label=f'Slope = {slope_a:.5f}', linestyle='--', color='black')
    plt.scatter(offset, Angles)
    plt.legend()
    plt.xlabel('offset (mm)')
    plt.ylabel('Δ Ellipe Angle from Symmetric (rad)')
    plt.title('1D Plot for Hole ' + Hole + ' ' + Pass + ' ' + Optics + ' ' + SecRot)
    plt.show()

#Last minuet notes (Applies to Find_Files.py, DrawElipse.py, nd Analysis.py):
#I am not a coder, so this code might be very inefficient, please feel free to change it around for future collection
#I am always available to contact if you have any questions, just let Professor Armstrong know and he can give you the information to reach out
#Best wishes and GL!  -Evan Jackson

QuantifyChangingOffsets(Hole = '72', Pass = 'p2', Optics = 'Optics2', xvalue = 'r_prime', yvalue = 'phi_prime', Type = 'Normal')
QuantifyChangingOffsets(Hole = '72', Pass = 'p2', Optics = 'Optics2', xvalue = 'r_prime', yvalue = 'phi_prime')
QuantifyChangingOffsets(Hole = '72', Pass = 'p2', Optics = 'Optics2', xvalue = 'r_prime', yvalue = 'phi_prime', Type = 'asdfsdfsdfa')
QuantifyChangingOffsets(Hole = '72', Pass = 'p2', Optics = 'Optics2', xvalue = 'r_prime', yvalue = 'phi_prime', Type = 'Even')
CompareOptics(Hole = '12', Pass = 'p3', Displacment = 'Symmetric', xvalue = 'gem_r', yvalue = 'gem_ph')
XandYplots(Hole = '72', Pass = 'p2', Optics = 'Optics2', Type = 'Normal')
QuantifyChangingOffsets(Hole = '12', Pass = 'p1', Optics = 'Optics2', xvalue = 'r_prime', yvalue = 'phi_prime', Type = 'Normal')
