#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Spectrophotometry program used for our mystery mixture lab in AP Chem.

Run it from the command line as `python spectrophotometry.py data_file.csv`.
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
