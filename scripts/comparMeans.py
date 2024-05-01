#import modules
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import numpy as np

#i don't use this but i'm keeping it here so that i remember the exact names of each column
colnames = ['hole_id', 'hole_center_r', 'hole_ph_offset', 'ideal_r_mean', 'ideal_r_stdDev', 'ideal_ph_mean', 'ideal_ph_stdDev', 'asymmetric_r_mean', 'asymmetric_r_stdDev', 'asymmetric_ph_mean', 'asymmetric_ph_stdDev']

#list of numbers for each hole
#hole_numbers = ['11', '12', '13', '21', '22', '23', '31', '41', '42', '51', '52', '53', '61', '62', '71', '72']

hole_numbers = [13, 12, 11, 23, 22, 21, 31, 42, 41, 53, 52, 51, 62, 61, 71, 72]
hole_center = [84.5,68,42,75,60,39,80,70,50,80,63,39,75,53,84.5,84.5]

#list so that each hole has a "category"
categories = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

#list of 16 distinct colors
colormap = np.array(['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000'])

#define number of rows (number of holes) and number of columns
rows = 16
cols = 1

#csv files to read in
filename_worst = 'opticsMatrix/FieldMapStudy/SieveHoleImageAnalysis_worstCase.csv'
filename_real = 'opticsMatrix/FieldMapStudy/SieveHoleImageAnalysis.csv'

#read csv and define mean difference columns
df = pd.read_csv(filename_worst)
df['hole_id']=hole_numbers
df['hole_center_r']=hole_center
df["r_mean_difference"] = (df["ideal_r_mean"] - df["asymmetric_r_mean"]).abs()
df["ph_mean_difference"] = (df["ideal_ph_mean"] - df["asymmetric_ph_mean"]).abs()

df2 = pd.read_csv(filename_real)
df2['hole_id']=hole_numbers
df2['hole_center_r']=hole_center
df2["r_mean_difference"] = (df2["ideal_r_mean"] - df2["asymmetric_r_mean"]).abs()
df2["ph_mean_difference"] = (df2["ideal_ph_mean"] - df2["asymmetric_ph_mean"]).abs()

#first figure is a color map

#create figures with subplots
fig = plt.figure(1, figsize = (9,6))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132, sharex=ax1, sharey=ax1) #both subplots have the same axes
ax3 = fig.add_subplot(133)

#define scatter plots with the color map colors assigned to each category
ax1.scatter(df["hole_center_r"], df["r_mean_difference"], c = colormap[categories])
ax2.scatter(df2["hole_center_r"], df2["r_mean_difference"], c = colormap[categories])

#define x axis tick marks
ax1.xaxis.set_ticks(np.arange(35, 86, 5))

#make new dataframe that is just the hole id numbers
df3 = df['hole_id'].copy()

#set the x and y limits based on the number of rows and columns
ax3.set_ylim(-1, rows + 1)
ax3.set_xlim(0, cols + 0.5)

#right out the values from the hole id dataframe into a column and color each entry the same way you colored the scatterplot
for row in range(rows):
    d = df3.iloc[row]
    ax3.text(x=0.5, y=15-row, s=d, va='center', ha='center', c = colormap[row])

#add title about text table and delete axes so that it looks like a table instead of a plot
ax3.text(0.5, 15.75, 'Hole Number', weight='bold', ha='center')
ax3.axis('off')

#set the titles for the subplots
ax1.set_title('Worst Case Asymmetric')
ax2.set_title('Realistic Asymmetric')

#set axis labels that are shared by both subplots
fig.supxlabel('Radial Location of Sieve Hole Center [mm]', fontsize = 12, ha = 'right')
fig.supylabel('Difference in Mean Values of Radial Hit Location on GEM1 [mm]', fontsize = 10)


#second figure has annotated points. I made both because each version is hard to read in its own way
fig2 = plt.figure(2, figsize = (8,6))
ax12 = fig2.add_subplot(121)
ax22 = fig2.add_subplot(122, sharex=ax12, sharey=ax12) #both subplots have the same axes

#define scatter plots with the color map colors assigned to each category
ax12.scatter(df["hole_center_r"], df["r_mean_difference"])
ax22.scatter(df2["hole_center_r"], df2["r_mean_difference"])

#define x axis tick marks
ax12.xaxis.set_ticks(np.arange(35, 86, 5))

#annotate each point with value from hole_numbers list
for idx, row in df.iterrows():
    ax12.annotate(row['hole_id'].astype('int'), (row['hole_center_r'], row['r_mean_difference']), xytext = (-5, 5), textcoords = 'offset points')

for idx, row in df2.iterrows():
    ax22.annotate(row['hole_id'].astype('int'), (row['hole_center_r'], row['r_mean_difference']), xytext = (5, -5), textcoords = 'offset points')

#set the titles for the subplots
ax12.set_title('Worst Case Asymmetric')
ax22.set_title('Realistic Asymmetric')

fig2.supxlabel('Radial Location of Sieve Hole Center [mm]', fontsize = 12)
fig2.supylabel('Difference in Mean Values of Radial Hit Location on GEM1 [mm]', fontsize = 10)

fig.savefig('opticsMatrix/FieldMapStudy/SieveHoleImageAnalysis_CompareMeans_color.png', format='png')
fig2.savefig('opticsMatrix/FieldMapStudy/SieveHoleImageAnalysis_CompareMeans_enumerate.png', format='png')

#The following code works, but I need to deal with physics issue first

#new data frame that only looks at symmetry pairs

#holes 21 and 51 : indices 5 and 11
#holes 31 and 53 : indices 6 and 9
#holes 23 and 62 : indices 3 and 12
#holes 71 and 72 : indices 14 and 15

#define new dataframes with only rows for each pair (worst case)
df_pair_2151 = df.loc[[5,11],:]
df_pair_3153 = df.loc[[6,9],:]
df_pair_2362 = df.loc[[3,12],:]
df_pair_7172 = df.loc[[14,15],:]

#define new dataframes with only rows for each pair (realistic asym)
df2_pair_2151 = df2.loc[[5,11],:]
df2_pair_3153 = df2.loc[[6,9],:]
df2_pair_2362 = df2.loc[[3,12],:]
df2_pair_7172 = df2.loc[[14,15],:]

#define figure and subplots
fig3 = plt.figure(3)
ax13 = fig3.add_subplot(111)

#scatterplots for each field map
ax13.scatter(df_pair_2151['ideal_r_mean'], df_pair_2151['hole_center_r'], c = 'b', label = 'Ideal')
ax13.scatter(df2_pair_2151['asymmetric_r_mean'], df2_pair_2151['hole_center_r'], c = 'g', label = 'Realistic Asym')
ax13.scatter(df_pair_2151['asymmetric_r_mean'], df_pair_2151['hole_center_r'], c = 'r', label = 'Worst Case Asym')

ax13.set_title('Holes 21 and 51')
ax13.set_xlabel('Mean Radial Location at GEM1 [mm]')
ax13.set_ylabel('Radial Location of Sieve Hole Center [mm]')
ax13.legend()

plt.show()














