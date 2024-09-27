import argparse
import sys, string
import os
import argparse
import ast
import glob
import math
from  ConfigParser import *
from ROOT import TFile, TNtuple
from array import array

def CSVReader(inputdirectory,outputdirectory,dataname):

   #Read file 
   filelist       = glob.glob(inputdirectory+"/"+dataname+"/*.csv")
   outputfilename = outputdirectory+"/"+dataname+".txt"
   if len(filelist)>1: print "[WARNING] More than two files in %s"%dataname

   #Format [id,theoretical,measured]
   t_list = []
   b_list = []
   l_list = []
   r_list = []
   h_list = []
   w_list = []
   #Read file lines
   for file in filelist:
        with open(file, "r") as my_input_file:
            for line in my_input_file:
                line = line.split(",", 10)
                if 'top' in line:                             
                    t_list.append([" ".join(line[0]), round( float(line[4]), 3), round( float(line[6]), 3) , round( float(line[8]), 3) ] )
                if 'bot' in line:         
                    b_list.append([" ".join(line[0]), round( float(line[4]), 3), round( float(line[6]), 3) , round( float(line[8]), 3) ] )
                if 'left' in line:         
                    l_list.append([" ".join(line[0]), round( float(line[4]), 3), round( float(line[6]), 3) , round( float(line[8]), 3) ] )
                if 'right' in line:         
                    r_list.append([" ".join(line[0]), round( float(line[4]), 3), round( float(line[6]), 3) , round( float(line[8]), 3) ] )
                if 'height' in line:
                    h_list.append([" ".join(line[0]), round( float(line[5]), 3), round( float(line[7]), 3) , round( float(line[9]), 3) ] )
                if 'width' in line:
                    w_list.append([" ".join(line[0]), round( float(line[5]), 3), round( float(line[7]), 3) , round( float(line[9]), 3) ] )      
   with open(outputfilename, "w") as my_output_file:
       my_output_file.write("  {0:3}  {1:6}  {2:6}  {3:6}  {4:6}  {5:6}  {6:6}  {7:6}  {8:6}  {9:6}  {10:6}  {11:6}  {12:6} {13:6}  {14:6}  {15:6}  {16:6}  {17:6}  {18:6}".format("id","top_rw","top_ms","top_th","bot_rw","bot_ms","bot_th","lft_rw", "lft_ms","lft_th","rgt_rw","rgt_ms", "rgt_th","hgt_rw", "hgt_ms", "hgt_th","wth_rw", "wth_ms", "wth_th") + "\n")
       for k in range(0, len(t_list) ):
                     my_output_file.write("  {0:3}".format(str(k) ) )
                     my_output_file.write("  {0:6}  {1:6}  {2:6}".format(str(t_list[k][1]), str(t_list[k][2]),str(t_list[k][3]) ))
                     my_output_file.write("  {0:6}  {1:6}  {2:6}".format(str(b_list[k][1]), str(b_list[k][2]),str(b_list[k][3]) ))           
                     my_output_file.write("  {0:6}  {1:6}  {2:6}".format(str(l_list[k][1]), str(l_list[k][2]),str(l_list[k][3]) ))   
                     my_output_file.write("  {0:6}  {1:6}  {2:6}".format(str(r_list[k][1]), str(r_list[k][2]),str(r_list[k][3]) ))
                     my_output_file.write("  {0:6}  {1:6}  {2:6}".format(str(h_list[k][1]), str(h_list[k][2]),str(h_list[k][3]) ))
                     my_output_file.write("  {0:6}  {1:6}  {2:6}".format(str(w_list[k][1]), str(w_list[k][2]),str(w_list[k][3]) )+ "\n")
       print('[INFO] File '+outputfilename+ ' successfully written')

def MakeNtuple(inputdirectory,outputdirectory,dataname):
     inputname  = inputdirectory+"/"+dataname+".txt"
     outputname = outputdirectory+"/"+dataname+".root"

     ifn = '%s'%inputname
     ofn = '%s'%outputname
     infile = open( ifn, 'r' )
     lines  = infile.readlines()
     labels = string.split( lines[0] )
     outfile = TFile( ofn, 'RECREATE', 'ROOT file with an NTuple' )
     ntuple  = TNtuple( 'tilentuple', 'tilentuple', string.join( labels, ':') )
     for line in lines[1:]:
         words = string.split( line )
         values = [float(i) for i in words]
         row = array("f",values)
         ntuple.Fill(row)
     outfile.Write()
     print('[INFO] File '+outputname+ ' successfully written')

#Get input/output information
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--config' ,  dest='cfgfile',  help='Name of config file',  required = True)
args            = parser.parse_args()
configfilename  = args.cfgfile

print "[INFO] Reading configuration file . . ."
cfgparser = ConfigParser()
cfgparser.read('%s'%configfilename)
print "    -The input directories:"
input_dir_dat    = ast.literal_eval(cfgparser.get("dataconfiguration","input_dir_dat"))
print "      *",input_dir_dat
input_dir_cal    = ast.literal_eval(cfgparser.get("dataconfiguration","input_dir_cal"))
print "      *",input_dir_cal
print "    -The output directory:"
output_dir_dat   = ast.literal_eval(cfgparser.get("dataconfiguration","output_dir_dat"))
print "      *",output_dir_dat
print "    -The output directory:"
output_dir_cal   = ast.literal_eval(cfgparser.get("dataconfiguration","output_dir_cal"))
print "      *",output_dir_cal
print "    -The list of data files:"
data_dat         = ast.literal_eval(cfgparser.get("dataconfiguration","data_dat"))
for x in range(len(data_dat)): print "      *",data_dat[x]
print "    -The list of data files:"
data_cal         = ast.literal_eval(cfgparser.get("dataconfiguration","data_cal"))
for x in range(len(data_cal)): print "      *",data_cal[x]

#Make directories
if not os.path.isdir("ntuples"):
   os.makedirs("ntuples")
if not os.path.isdir("%s"%output_dir_dat):
   os.makedirs("%s"%output_dir_dat)
if not os.path.isdir("%s"%output_dir_cal):
   os.makedirs("%s"%output_dir_cal)

#Process dataset
for k in range( 0,len(data_dat)):
    print "[INFO] Reading %s for plots"%data_dat[k]
    CSVReader(input_dir_dat+"/",output_dir_dat,data_dat[k])
#Process calibration
for k in range( 0,len(data_cal)):
    print "[INFO] Reading %s for calibration"%data_cal[k]
    CSVReader(input_dir_cal+"/",output_dir_cal,data_cal[k])

#Make root file for dataset
for k in range( 0,len(data_dat)):
    print "[INFO] Ntuple %s for plots"%data_dat[k]  
    MakeNtuple(output_dir_dat+"/",output_dir_dat,data_dat[k])

#Make root file for calibration
for k in range( 0,len(data_cal)):
    print "[INFO] Ntuple %s for calibration"%data_cal[k]  
    MakeNtuple(output_dir_cal+"/",output_dir_cal,data_cal[k])
