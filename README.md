#Spectrophotometry.py
To determine the composition of a mystery mixture consisting of various types of food coloring, I wrote this program that works with Vernier's Spectral Analysis software. It will determine the ratio between the concentrations of yellow, red, and blue are in the mystery solution given four spectrophotograms: a yellow, a red, a blue, and the mystery one.

One limitation of the program is that the wavelength values need to line up across the CSV table- thus all the data used must be collected at the same time.

To modify this program for use in other situations, the hard-coded maximum concentration variable could be changed. Further updates to the script could make it more generalized by allowing the use of a command-line flag to change this value.

### Usage
- Download the script from my Github page [here](https://github.com/michaelnoguera/spectrophotometry).
- Run the script in the terminal, providing your CSV export from Spectral Analysis as the first argument (replace `PATH_TO_YOUR_CSV_FILE` in the command below).

```bash
python spectrophotometry.py PATH_TO_YOUR_CSV_FILE
```

- Follow the prompts in the program to pair up your absorbance columns with the different colors.
- The relative concentrations will be printed directly to `stdout`. You can always pipe the output into a file as follows:

```bash
python spectrophotometry.py PATH_TO_YOUR_CSV_FILE > output.txt
```
