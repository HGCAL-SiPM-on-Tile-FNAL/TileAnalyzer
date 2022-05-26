# Tile Analyzer
Code to analyze tiles

## Install

Log in to the LPC machines
```
ssh -XY username@cmslpc-sl7.fnal.gov
```

Get code from git
````
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src
cmsenv
git clone https://github.com/HGCAL-SiPM-on-Tile-FNAL/TileAnalyzer 
cd TileAnalyzer 
````

## Convert CSV to ROOT files
Copy your *.csv files in folder named files, and then run the converter script to create a txt and a ROOT file
```` 
python scripts/CSVtoROOTconverter.py --input files/histos_DESY_May23.csv #for desy tiles
python scripts/CSVtoROOTconverter.py --input files/histos_calibration_May23.csv #for calibration tiles
````

## Make Plots
First step is to make 1d or 2d histograms. The code skeleton PyROOT-based using the script called histogrammer.py in the plotter folder. That script create a ROOT file with histograms, and put it in a folder called histograms
```` 
cd plotter
python histogrammer.py --inputfile ../files/calibration_May23.root --outputfile histos_calibration_May23.root        #for calibration tiles
python histogrammer.py --inputfile ../files/DESY_May23.root        --outputfile histos_DESY_May23.root               #for desy tiles
````

Then, the next step is plot your 1d and 2d histograms using the plotter.py. The instructions are inside the script. The plot are saved in the folders plots1d and plots2d.
```` 
python plotter.py
````