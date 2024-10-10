#import modules
import os
import pandas as pd

#This script will combine all CSV files in a directory into a new file in that same directory called "combined.csv".

#User input will define the path to the CSV files and an output file for the combined CSV file.
#Example: file_path = "output/Symmetric/Pass2_Optics1/"
file_path = input("Enter path to the folder of CSV files you would like to combine. This should be in the form /path/to/files/ \n")
output_file = file_path + "combined.csv"

#Make a list of all files in a directory.
file_list = os.listdir(file_path)
#print(file_list)

hole_list = ["11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73"]

single_hole_file_list = []

for hole in hole_list:
    for file in file_list:
        if hole in file:
            single_hole_file_list.append(file)

#print(single_hole_file_list)

#Combine data from all files in file_list into one data frame.
#df_concat = pd.concat([pd.read_csv(file_path+f) for f in file_list], ignore_index=True)
df_concat = pd.concat([pd.read_csv(file_path+f) for f in single_hole_file_list], ignore_index=True)

#Write the data frame to a CSV file.
df_concat.to_csv(output_file)
