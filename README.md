# Tile Analyzer
Code to analyze tiles

## Install

Log in to the LPC machines, setup singularity to SL7 and get in your nobackup area.
```
ssh -XY username@cmslpc-el9.fnal.gov
cmssw-el7 --bind /uscms_data
cd nobackup/
```

Get code from git. 
````
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src
cmsenv
git clone https://github.com/HGCAL-SiPM-on-Tile-FNAL/TileAnalyzer 
cd TileAnalyzer 
````
Note that this CMSSW version only works on SL7, so you have to run the singularity command (cmssw-el7) before you do cmsenv.

## Data processing
The PnP machine stores the tile dimensional data in .csv files. They must be copied to the data directory. If the data is used for dimensional calibration, they must be stored in the calibration folder. If the data are used for measurements, they must be stored in the dataset folder. As an example, I provided recent measurements of reference bare tiles used for calibration (Data_bare_T3435_OGP_1,  Data_bare_T3637_OGP_1, Data_bare_T3839_OGP_1, Data_bare_T4041_OGP_1). I also provided recent measurements of bare tiles (Data_bare_T3435_C1,  Data_bare_T3435_C2,	Data_bare_T3637_C1,  Data_bare_T3637_C2,	Data_bare_T3839_C1, Data_bare_T3839_C2,Data_bare_T4041_C1,Data_bare_T4041_C2). 

We can convert the data from .csv to root file using the CSVtoROOTconverterDefault.py script. The .cfg contains names of the tile data to be processed using the script. The output of the script is stored in the ntuples folder. It processes both calibration and measurement data.
```
python scripts/CSVtoROOTconverterDefault.py  --config config/configuration.cfg

```

## Histograms and graphs
We make ROOT histograms and graphs from the ntuples using the Histogrammer script. Similarly, we have to provide names of the tile data in the .cfg file. Note that we could also provide the expected values of the tile dimensions (See more in config file).
```
python scripts/Histogrammer.py  --config config/configuration.cfg

```

## Calibration plots
To derive the fits used to calibrate the PnP measurement. These fits are used in the machine to correct residual differences between the PnP measurement and the OGP reference measurement.
```
python scripts/calibration.py  --config config/configuration.cfg

```

## Measurement plots
To derive the plots associated to any PnP measurements
```
python scripts/plotter.py  --config config/configuration.cfg

```