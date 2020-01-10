#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Spectrophotometry program used for our mystery mixture lab in AP Chem.

Designed to work with CSV exports from Vernier's Graphical Analysis program. Required inputs are
a spectrophotogram for the unknown mystery mixture, pure yellow, pure red, and pure blue, and the 
ratio of yellow, red, and blue in the mixture will be output. Input data sets must all have the same 
wavelengths as dependent variables, as the program does not account for possible misalignments.

Run it from the command line as `python spectrophotometry.py data_file.csv`.

Dependencies
------------
- `Python 3`, written with 3.7.6, but should be compatible with older Python 3 versions.
- `pandas` library for data analysis
- `optimize` submodule of the `scipy` library
- `List` submodule of the `typing` library
'''

import sys  # system library, used to read in arguments, as this is a command line app
from typing import List # adds gradual typing support for List, IMO this should really be
# part of the programming language itself, like primitive typing is
import pandas as pd  # pandas library, allows manipulation of data in a table-like format
# science library, this subpackage contains the LM-BFGS-B implementation used
from scipy import optimize

# Parse the -h flag, which stands for "help"
if '-h' in sys.argv:
    print('\n\033[1;37mspectrophotometry.py by Michael Noguera\033[0m')
    print('\n\tFinds the ratio of the components in a color mixture based on their spectrophotograms, ')
    print('\tbased on the LM-BFGS-B algorithm for optimizing a multi-variable system.')
    print('\n\033[4;37mUsage:\033[0m')
    print('\t`python spectrophotometry.py data_file.csv`')
    print('\n\tThe csv file should be in the format exported from the Vernier Spectral Analysis app.')
    print('\n\033[4;37mOptions:\033[0m')
    print('\t-h \tdisplays this message and exits\n')
    quit()

# Read the file path provided by the user
filepath: str = sys.argv[1]

# Load the file at that location
df: pd.DataFrame = pd.read_csv(filepath)

###
# PARSE CSV DATA
###

# Rename first wavelength column, this one will be saved
df.rename(columns={df.columns[0]: "Wavelength"}, inplace=True)

# Delete redundant wavelength columns
df.drop(list(df.filter(regex='\:Wavelength\(nm\)')), axis=1, inplace=True)

# Remove all ":Absorbance" suffixes from column names
df.rename(columns=lambda s: s.replace(
    ":Absorbance", "").strip(), inplace=True)

# Try to automatically match columns with their contents
for column in df.columns:
    if "red" in column.lower():
        df.rename(columns={column: "Red"}, inplace=True)
    if "blue" in column.lower():
        df.rename(columns={column: "Blue"}, inplace=True)
    if "yellow" in column.lower():
        df.rename(columns={column: "Yellow"}, inplace=True)
    if "mystery" in column.lower():
        df.rename(columns={column: "Experimental"}, inplace=True)

# Match up missing columns
for column in ["Red", "Blue", "Yellow", "Experimental"]:
    if not column in df.columns: # a column is missing, make the user match it up
        print("These are your solutions. Please match the missing column by entering it's corresponding number.")
        print('\n'.join('{}: {}'.format(*k)
                        for k in enumerate(df.columns[1:], 1)))  # print out columns in a pretty way
        df.rename(
            columns={df.columns[int(input(column+" = ").strip())]: column}, inplace=True)  # rename descriptively based on user input
        print("\n")

# Put columns in order
df = df[["Wavelength", "Yellow", "Red", "Blue", "Experimental"]]

# Output table preview to the user
print(df.head())
print("...")

###
# Optimization routine
###

# Adjust for stock concentration being not equal to one unit per volume
stock_concentration: float = 12.00  # constant for stock solution concentration
df[['Yellow', 'Red', 'Blue']] = df[['Yellow', 'Red', 'Blue']].div(
    stock_concentration)  # divide all data values by stock sample concentration

# Optimize for best solution
def error(yrb: List[float]) -> float:
    ''' Function that calculates the total error for a given concentration combination.

    Arguments:
    yrb: List[float] -- A list containing the concentrations of [yellow, red, blue] in that order.

    Returns: the total least-squares error for that combination across all included wavelengths.
    '''
    ret: float = 0
    for (index, row) in df.iterrows():
        ret += ((row['Yellow']*yrb[0])+(row['Red']*yrb[1]) +
                (row['Blue']*yrb[2])-row['Experimental'])**2
    return ret

result: optimize.OptimizeResult = optimize.minimize(
    fun=error, x0=[2, 2, 2], bounds=[(0, 12), (0, 12), (0, 12)], method='L-BFGS-B')

# Output solution to user
print("\nSOLUTION FOUND (and pun intended)")
print("\033[1;33m"+str(round(dict(result.items())['x'][0], 3)) +
      "\033[0;33m\tparts yellow\033[0m")
print("\033[1;31m"+str(round(dict(result.items())['x'][1], 3)) +
      "\033[0;31m\tparts red\033[0m")
print("\033[1;34m"+str(round(dict(result.items())['x'][2], 3)) +
      "\033[0;34m\tparts blue\033[0m")
print("error of "+str(round(dict(result.items())['fun'], 3)))
