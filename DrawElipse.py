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

#This is where most of the plot/math generation happens

def DrawElipse(F1 = '', xaxis = '', yaxis = '', color = '', ax=None, label = ''):
    #Draws a single ellipes from a defined file
    if ax is None:
        fig, ax = plt.subplots()
    #First it makes the subplots for multiple plots in one and pandas reads the CSV base on xaxis and yaxis defined
    #Make sure xaxis and yaxis are the same as in the CSV or the code will error
    df = pd.read_csv(F1)
    df[xaxis] = pd.to_numeric(df[xaxis], errors='coerce')
    df[yaxis] = pd.to_numeric(df[yaxis], errors='coerce')
    df = df.dropna(subset=[xaxis, yaxis])
    xvalues = df[xaxis].dropna().tolist()
    yvalues = df[yaxis].dropna().tolist()
    xmean = np.mean(xvalues)
    ymean = np.mean(yvalues)
    #This point forward is some linear algebra and basic statistics to draw and define the ellipes. You can find more information on my thesis (It shouldn't be too hard to udnerstand)
    xStandDev = np.std(xvalues)
    yStandDev = np.std(yvalues)
    cov = np.cov(xvalues, yvalues)
    PCoeff = cov[0,1]/np.sqrt(cov[1,1] * cov[0,0])
    center_elipse = [xmean, ymean]
    n = 2.3
    HScale = (n * xStandDev)
    VScale = (n * yStandDev)
    HRad = np.sqrt(1 + PCoeff)
    VRad = np.sqrt(1 - PCoeff)
    ellipse = patches.Ellipse(xy = [0,0], width = (HRad * 2), height = (VRad * 2), fill=False, edgecolor = color, label = label)
    transf = transforms.Affine2D().rotate_deg(45).scale(HScale, VScale).translate(xmean, ymean)
    ellipse.set_transform(transf + ax.transData)
    ax.add_patch(ellipse)
    #Given that the plot does not center on the ellipse naturally we have to define the bounds of our plot. We can do this by making a range from each maximum and minimum values defined by "margin"
    #To simplify it further, if margin is bigger then the scale of the plot is bigger and if smaller vise versa
    #The bounds are then defined by LowX, LowY, HighX, HighY for future code
    margin = .5
    x_lower, x_upper = min(xvalues), max(xvalues)
    y_lower, y_upper = min(yvalues), max(yvalues)
    LowX = x_lower - margin * abs(x_upper - x_lower)
    HighX = x_upper + margin * abs(x_upper - x_lower)
    LowY = y_lower - margin * abs(y_upper - y_lower)
    HighY = y_upper + margin * abs(y_upper - y_lower)
    rangeX = abs(HighX - LowX)
    rangeY = abs(HighY - LowY)
    #More linear algebra for ellipse to define C and focal points (Basic ellipse values)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    SemiMajor = np.sqrt(eigenvalues[sorted_indices[0]])
    SemiMinor = np.sqrt(eigenvalues[sorted_indices[1]])
    MajorAxisVector = eigenvectors[:, sorted_indices[0]]
    c = np.sqrt((np.square(SemiMajor) - np.square(SemiMinor)))
    theta = np.arctan2(MajorAxisVector[1], MajorAxisVector[0])
    Focalx = [xmean + (c * np.cos(theta)), xmean - (c * np.cos(theta))]
    Focaly = [ymean + (c * np.sin(theta)), ymean - (c * np.sin(theta))]
    plt.scatter(Focalx,Focaly, color=color)
    plt.plot(Focalx, Focaly, marker='o', color=color)
    #The code below makes a scatter plot as well if you want to see the ellipse with the scattered data
    #plt.scatter(xvalues,yvalues, color = color)
    ax.set_xlim(LowX, HighX)
    ax.set_ylim(LowY, HighY)
    return(ax, LowX, HighX, LowY, HighY)

#The same as the first function but assumes the file has already been processed using FindFiles. I believe I added this because file name processing became a little more complex so I just wanted a function you can insert datasets into for processing
#The reason for this seperation is so if I wanted to understand a single ellipse plot I could run DrawElipse by itself.
#This can be a tad confusing so if you decide to combine it I can see a benifit but I also don't see a downside to having both for verification reasons.
def DrawAnyElipse(xvalues = '', yvalues = '', color = 'r', ax=None, label = ''):
    if ax is None:
        fig, ax = plt.subplots()
    xmean = np.mean(xvalues)
    ymean = np.mean(yvalues)
    xStandDev = np.std(xvalues)
    yStandDev = np.std(yvalues)
    cov = np.cov(xvalues, yvalues)
    PCoeff = cov[0,1]/np.sqrt(cov[1,1] * cov[0,0])
    center_elipse = [xmean, ymean]
    n = 2.3
    HScale = (n * xStandDev)
    VScale = (n * yStandDev)
    HRad = np.sqrt(1 + PCoeff)
    VRad = np.sqrt(1 - PCoeff)
    ellipse = patches.Ellipse(xy = [0,0], width = (HRad * 2), height = (VRad * 2), fill=False, edgecolor = color, label = label)
    transf = transforms.Affine2D().rotate_deg(45).scale(HScale, VScale).translate(xmean, ymean)
    ellipse.set_transform(transf + ax.transData)
    ax.add_patch(ellipse)
    margin = .5
    x_lower, x_upper = min(xvalues), max(xvalues)
    y_lower, y_upper = min(yvalues), max(yvalues)
    LowX = x_lower - margin * abs(x_upper - x_lower)
    HighX = x_upper + margin * abs(x_upper - x_lower)
    LowY = y_lower - margin * abs(y_upper - y_lower)
    HighY = y_upper + margin * abs(y_upper - y_lower)
    rangeX = abs(HighX - LowX)
    rangeY = abs(HighY - LowY)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    SemiMajor = np.sqrt(eigenvalues[sorted_indices[0]])
    SemiMinor = np.sqrt(eigenvalues[sorted_indices[1]])
    MajorAxisVector = eigenvectors[:, sorted_indices[0]]
    c = np.sqrt((np.square(SemiMajor) - np.square(SemiMinor)))
    theta = np.arctan2(MajorAxisVector[1], MajorAxisVector[0])
    Focalx = [xmean + (c * np.cos(theta)), xmean - (c * np.cos(theta))]
    Focaly = [ymean + (c * np.sin(theta)), ymean - (c * np.sin(theta))]
    plt.scatter(Focalx,Focaly)
    plt.plot(Focalx, Focaly, marker='o', color=color)
    ax.set_xlim(LowX, HighX)
    ax.set_ylim(LowY, HighY)
    return(ax, LowX, HighX, LowY, HighY)

#This code simply takes the math of DrawEllipse but does not plot anything. Istead is takes the raw values, usefull for future 1D plots and calculation
def GrabValues(F1 = '', xaxis = '', yaxis = ''):
    df = pd.read_csv(F1)
    df[xaxis] = pd.to_numeric(df[xaxis], errors='coerce')
    df[yaxis] = pd.to_numeric(df[yaxis], errors='coerce')
    df = df.dropna(subset=[xaxis, yaxis])
    xvalues = df[xaxis].dropna().tolist()
    yvalues = df[yaxis].dropna().tolist()
    xmean = np.mean(xvalues)
    ymean = np.mean(yvalues)
    cov = np.cov(xvalues, yvalues)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    SemiMajor = np.sqrt(eigenvalues[sorted_indices[0]])
    SemiMinor = np.sqrt(eigenvalues[sorted_indices[1]])
    MajorAxisVector = eigenvectors[:, sorted_indices[0]]
    c = np.sqrt((np.square(SemiMajor) - np.square(SemiMinor)))
    theta = np.arctan2(MajorAxisVector[1], MajorAxisVector[0])
    Focalx = [xmean + (c * np.cos(theta)), xmean - (c * np.cos(theta))]
    Focaly = [ymean + (c * np.sin(theta)), ymean - (c * np.sin(theta))]
    xerr = np.std(xvalues) / (np.sqrt(len(xvalues)))
    yerr = np.std(yvalues)/ (np.sqrt(len(yvalues)))
    return(xmean, ymean, xerr, yerr, Focalx, Focaly)

#Same reason for having two as before: GrabValues needs a filename and GrabAnyValues does not.
def GrabAnyValues(xvalues = '', yvalues = ''):
    xmean = np.mean(xvalues)
    ymean = np.mean(yvalues)
    cov = np.cov(xvalues, yvalues)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    SemiMajor = np.sqrt(eigenvalues[sorted_indices[0]])
    SemiMinor = np.sqrt(eigenvalues[sorted_indices[1]])
    MajorAxisVector = eigenvectors[:, sorted_indices[0]]
    c = np.sqrt((np.square(SemiMajor) - np.square(SemiMinor)))
    theta = np.arctan2(MajorAxisVector[1], MajorAxisVector[0])
    Focalx = [xmean + (c * np.cos(theta)), xmean - (c * np.cos(theta))]
    Focaly = [ymean + (c * np.sin(theta)), ymean - (c * np.sin(theta))]
    return(xmean, ymean, Focalx, Focaly, theta)

#This code takes multiple ellipses and complies them into a single plot
#We can see that a new value is defined as Type, This value is simply used to only use Even plots
#Some maps re generated in groups of four not seven, so defining type as even will only define four quntitie in2mm, symmetric, out2mm, and out4mm
#Any other input will just do the regular seven field maps
def MakeElipseMap(Hole = '', Pass = '', Optics = '',SecRot = '', xvalue = '', yvalue = '', Type = '', SecRotE = ''):
    if 'Even' in Type:
        types = ['in2mm', 'Symmetric', 'out2mm', 'out4mm']
        colors = ['#ff0000', '#cccc00', '#258e8e', '#730099']
        offset = [-2, 0, 2, 4]
    else:
        types = ['in2mm', 'in1mm', 'Symmetric', 'out1mm', 'out2mm', 'out3mm', 'out4mm']
        colors = ['#ff0000', '#ff8000', '#cccc00', 'green', '#258e8e', 'blue', '#730099']
        offset = [-2, -1, 0, 1, 2, 3, 4]
    LowX_Values = []
    HighX_Values = []
    LowY_Values = []
    HighY_Values = []
    fig, ax = plt.subplots()
    for type, color in zip(types, colors):
        file_path = FindFiles(type + '' + Pass + '' + Optics + SecRotE) + Hole + '.csv'
        ax, LowX, HighX, LowY, HighY = DrawElipse(F1=file_path, xaxis=xvalue, yaxis=yvalue, color=color, ax=ax, label=type)
        LowX_Values.append(LowX)
        HighX_Values.append(HighX)
        LowY_Values.append(LowY)
        HighY_Values.append(HighY)
    #This takes all the LowX, LowY, HighX, HighY and finds to extreams to define the dimensions of this compiled plot
    ax.set_xlim(min(LowX_Values), max(HighX_Values))
    ax.set_ylim(min(LowY_Values), max(HighY_Values))
    ax.set_xlabel(xvalue + ' (mm)')
    ax.set_ylabel(yvalue+ ' (rad)')
    ax.set_title(Pass + ' Hole ' + Hole + ' ' + yvalue + ' by ' + xvalue + ' graph')
    ax.legend(title="Offset")
    plt.show()

#This simply makes a scatter plot
def MakeScatter(F1 = '', xaxis = '', yaxis = '', ax=None, color = '', label = ''):
    if ax is None:
        fig, ax = plt.subplots()
    df = pd.read_csv(F1)
    df[xaxis] = pd.to_numeric(df[xaxis], errors='coerce')
    df[yaxis] = pd.to_numeric(df[yaxis], errors='coerce')
    df = df.dropna(subset=[xaxis, yaxis])
    xvalues = df[xaxis].dropna().tolist()
    yvalues = df[yaxis].dropna().tolist()
    ax.scatter(xvalues,yvalues, label = label, color = color)
    return ax

#This will simplify the ellipses into the means and focal points decribed in my thesis
#It is the same as the ellipse plots but defines different variables to be plotted
def MakeMeans(F1 = '', xaxis = '', yaxis = '', ax=None, color = '', label = ''):
    if ax is None:
        fig, ax = plt.subplots()
    df = pd.read_csv(F1)
    df[xaxis] = pd.to_numeric(df[xaxis], errors='coerce')
    df[yaxis] = pd.to_numeric(df[yaxis], errors='coerce')
    df = df.dropna(subset=[xaxis, yaxis])
    xvalues = df[xaxis].dropna().tolist()
    yvalues = df[yaxis].dropna().tolist()
    xmean = np.mean(xvalues)
    ymean = np.mean(yvalues)
    xStandDev = np.std(xvalues)
    yStandDev = np.std(yvalues)
    xmerr = xStandDev / np.sqrt(len(xvalues))
    ymerr = yStandDev / np.sqrt(len(yvalues))
    cov = np.cov(xvalues, yvalues)
    PCoeff = cov[0,1]/np.sqrt(cov[0,0] * cov[1,1])
    n = 2.3
    HScale = (n * xStandDev)
    VScale = (n * yStandDev)
    HRad = np.sqrt(1 + PCoeff)
    VRad = np.sqrt(1 - PCoeff)
    rangle = 0.5 * np.arctan((2 * cov[0,1]) / (cov[0,0] - cov[1,1]))
    angle = np.degrees(rangle)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    SemiMajor = np.sqrt(max(eigenvalues))
    SemiMinor = np.sqrt(min(eigenvalues))
    c = np.sqrt((np.square(SemiMajor) + np.square(SemiMinor)))
    theta = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0])
    Focalx = [xmean + (c * np.cos(theta)), xmean - (c * np.cos(theta))]
    Focaly = [ymean + (c * np.sin(theta)), ymean - (c * np.sin(theta))]
    plt.plot(Focalx, Focaly, marker='o', color=color)
    theta = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0])
    center_elipse = [xmean, ymean]
    ax.errorbar(xmean, ymean, xerr=xmerr, yerr=ymerr, fmt='o', color=color, markersize=10, label=label, capsize=5)
    return ax
