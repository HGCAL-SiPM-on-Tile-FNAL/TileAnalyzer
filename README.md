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
Copy your *.csv files in folder named files, and then run the converter script
```` 
python scripts/CSVtoROOTconverter.py --input files/*.csv #It will create a txt and a ROOT file
````