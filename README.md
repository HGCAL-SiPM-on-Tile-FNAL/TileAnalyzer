Get code from git
````
cmsrel CMSSW_10_6_19_patch2
cd CMSSW_10_6_19_patch2/src
cmsenv
git clone https://github.com/HGCAL-SiPM-on-Tile-FNAL/TileAnalyzer 
cd TileAnalyzer 
````

## Processed raw PnP data 
First copy all systematic data folder into data/raw/. This could be both default or multishot 
```
scp -r Data_* username@cmslpc-sl7.fnal.gov/yourlocaladdress/data/raw 

```
Then, processed the data into organized folders. The output will be in data/processed. The config file defines what folder you want to process. The tag is the name of the output folder.
```
python scripts/process_rawdata.py --config config/configuration_default.cfg   --tag Default
python scripts/process_rawdata.py --config config/configuration_multishot.cfg --tag Multishot
```

## Convert CSV to ROOT files
Now, it is time to use the processed files (CSV or shots) into ROOT files. Note that this is super quick for the default. However, for the multishot this is the part where we measure the four edges using fits. We can use the cores available in the LPC nodes to do it (there is up to 8 cores available). To maximize speed, you should assign one folder per node. The number of points per folder that you want to measure is defined in the config file. One can also pick between initial an final round of shots for this in the config file.  
```` 
python scripts/CSVtoROOTconverterDefault.py   --config config/configuration_default.cfg   --tag Default
python scripts/CSVtoROOTconverterMultishot.py --config config/configuration_multishot.cfg --tag Multishot
````
## Make Histograms and plot them
The script used to make 1d or 2d histogram is called Histogrammer.py. The code skeleton is based PyROOT. That script creates a ROOT file with histograms, and put it in a folder called histograms.
```` 
python scripts/Histogrammer.py --config config/configuration_default.cfg   --tag Default
python scripts/Histogrammer.py --config config/configuration_multishot.cfg --tag Multishot
````
Then, the next step is plot your 1d and 2d histograms using the plotter.py. The instructions are inside the script, make sure that you point to the correct names when running default vs multishot plots. The plot are saved in the folders plots1d and plots2d. These folders are inside the plots/<tag> folder.
```` 
python scripts/plotter.py --config config/configuration_default.cfg   --tag Default
python scripts/plotter.py --config config/configuration_multishot.cfg --tag Multishot
````

## Multishot Algorithm Development Script
There is a script (Reconstruction_Multishot.py) that runs the whole multishot routine including all supporting plots. It is located in the reconstruction folder. It will run your algorithm on shots in a folder called examples/point_1. Just always make sure the noozle location in the script is the same as the csv file. To run it is very easy!
```` 
cd reconstruction
python Reconstruction_Multishot.py
