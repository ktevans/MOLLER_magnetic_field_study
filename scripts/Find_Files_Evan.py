#import modules
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import numpy as np

#This code defines a single function FindFiles which simply makes the file path for the field maps we want to understand
#This code is fairly basic and can probably be refined if you wish
#Some of the file names are different due to CSV generation code changing midway though the project which is why pass 1 and 5 have different names
#It is important that this code can find files when you define the file name exactly and when you simply define a bunch of parameters (Look at the examples at the bottom and run them)
#It is also important to remember this code looks for specific phrases in the string so when inputing variables in other function these have to be specific
#These are defined as Pass(px), Target(Opticsx (or LH2 I think)), Offset (inxmm/outxmm (for whatever direction the offset is) and symmetric for so offset), and Sector Rotation (SecRotx) where x is a viable value

def FindFiles(Filename1):
    #Define the begining of the location
    begining = '../output/'
    File = None
    #Elif code to slowly sort the file by what we want
    #Filename2 makes the file name if we haven't defined it (but needs .csv) and File makes the path
    if 'Symmetric' in Filename1:
        File = begining + 'Symmetric/'
        Filename2 = 'Symmetric_'
    elif 'out' in Filename1:
        if 'out1mm' in Filename1:
            File = begining + 'A_out1mm/'
            if not any(substring in Filename1 for substring in ['SecRot', 'p1', 'p5', 'Pass1', 'Pass5']):
                Filename2 = 'A_out1mm_'
            else:
                Filename2 = 'A1mm_outward_'
        elif 'out2mm' in Filename1:
            File = begining + 'A_out2mm/'
            if not any(substring in Filename1 for substring in ['SecRot', 'p1', 'p5', 'Pass1', 'Pass5']):
                Filename2 = 'A_out2mm_'
            else:
                Filename2 = 'A2mm_outward_'
        elif 'out3mm' in Filename1:
            File = begining + 'A_out3mm/'
            if not any(substring in Filename1 for substring in ['SecRot', 'p1', 'p5', 'Pass1', 'Pass5']):
                Filename2 = 'A_out3mm_'
            else:
                Filename2 = 'A3mm_outward_'
        elif 'out4mm' in Filename1:
            File = begining + 'A_out4mm/'
            if not any(substring in Filename1 for substring in ['SecRot', 'p1', 'p5', 'Pass1', 'Pass5']):
                Filename2 = 'A_out4mm_'
            else:
                Filename2 = 'A4mm_outward_'
    elif 'in' in Filename1:
        if 'in1mm' in Filename1:
            File = begining + 'A_in1mm/'
            if not any(substring in Filename1 for substring in ['SecRot', 'p1', 'p5', 'Pass1', 'Pass5']):
                Filename2 = 'A_in1mm_'
            else:
                Filename2 = 'A1mm_inward_'
        elif 'in2mm' in Filename1:
            File = begining + 'A_in2mm/'
            if not any(substring in Filename1 for substring in ['SecRot', 'p1', 'p5', 'Pass1', 'Pass5']):
                Filename2 = 'A_in2mm_'
            else:
                Filename2 = 'A2mm_inward_'
    #If nothing is found print no file found
    if File is None:
        print('No File Found (offset)')
        return None
    #Same filtering for passes now
    if 'p1' in Filename1 or 'pass1' in Filename1:
        if 'Optics1' in Filename1:
            File = File + 'Pass1_Optics1/'
            Filename2 = Filename2 + 'p1_Optics1_'
        elif 'Optics2' in Filename1:
            File = File + 'Pass1_Optics2/'
            Filename2 = Filename2 + 'p1_Optics2_'
        elif 'Optics3' in Filename1:
            File = File + 'Pass1_Optics3/'
            Filename2 = Filename2 + 'p1_Optics3_'
        else:
            print('No File Found (o)')
            return None
    elif 'p5' in Filename1 or 'pass5' in Filename1:
        if 'Optics1' in Filename1:
            File = File + 'Pass5_Optics1/'
            Filename2 = Filename2 + 'p5_Optics1_'
        elif 'Optics2' in Filename1:
            File = File + 'Pass5_Optics2/'
            Filename2 = Filename2 + 'p5_Optics2_'
        elif 'Optics3' in Filename1:
            File = File + 'Pass5_Optics3/'
            Filename2 = Filename2 + 'p5_Optics3_'
        else:
            print('No File Found (o)')
            return None
    elif 'p2' in Filename1 or 'pass2' in Filename1:
        if 'Optics1' in Filename1:
            File = File + 'Pass2_Optics1/'
            Filename2 = Filename2 + 'p2_C12_Optics1_'
        elif 'Optics2' in Filename1:
            File = File + 'Pass2_Optics2/'
            Filename2 = Filename2 + 'p2_Optics2_'
        elif 'Optics3' in Filename1:
            File = File + 'Pass2_Optics3/'
            Filename2 = Filename2 + 'p2_Optics3_'
        else:
            print('No File Found (o)')
            return None
    elif 'p3' in Filename1 or 'pass3' in Filename1:
        if 'Optics1' in Filename1:
            File = File + 'Pass3_Optics1/'
            Filename2 = Filename2 + 'p3_C12_Optics1_'
        elif 'Optics2' in Filename1:
            File = File + 'Pass3_Optics2/'
            Filename2 = Filename2 + 'p3_Optics2_'
        elif 'Optics3' in Filename1:
            File = File + 'Pass3_Optics3/'
            Filename2 = Filename2 + 'p3_Optics3_'
        else:
            print('No File Found (o)')
            return None
    else:
        print('No File Found (p)')
        return None

    #The naming convention for Pass1 and Pass5 files had 0SecRot in them due to new CSSV generator so I had to add this line.
    if any(substring in Filename1 for substring in ['p1', 'p5', 'Pass1', 'Pass5']):
        Filename2 += '0SecRot_'
    #If there is a sector rotation add it
    for i in range(1, 7):
        if f"{i}SecRot" in Filename1:
            File += f"{i}SecRot/"
            Filename2 += f"{i}SecRot_"
            break
    #If there was a .csv at the end it expects us to have inputed the full file name so it just adds the path to it. If there was no .csv then it expectes a random collection of variables so it generated the file name and adds it.
    if not Filename1.endswith('.csv'):
        Filename2 = File + Filename2
        return(Filename2)
    else:
        File = File + Filename1
        return File


print(FindFiles('in1mmp2Optics2'))
print(FindFiles('A_out3mm_p3_C12_Optics1_SecRot1_11.csv'))
print(FindFiles('Symmetricp2Optics2'))
