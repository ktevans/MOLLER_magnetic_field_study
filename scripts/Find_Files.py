#import modules
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import numpy as np

def FindFiles(Filename1):
    begining = '../output/'
    File = None

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

    if File is None:
        print('No File Found (offset)')
        return None

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

    if any(substring in Filename1 for substring in ['p1', 'p5', 'Pass1', 'Pass5']):
        Filename2 += '0SecRot_'

    for i in range(1, 7):
        if f"{i}SecRot" in Filename1:
            File += f"{i}SecRot/"
            Filename2 += f"{i}SecRot_"
            break

    if not Filename1.endswith('.csv'):
        Filename2 = File + Filename2
        return(Filename2)
    else:
        File = File + Filename1
        return File


print(FindFiles('in1mmp2Optics2'))
print(FindFiles('A_out3mm_p3_C12_Optics1_SecRot1_11.csv'))
print(FindFiles('Symmetricp2Optics2'))
