import argparse
import sys, string

import os
import argparse
import ast
import glob
import math
from  ConfigParser import *
from ROOT import TFile, TNtuple

def CSVReader(inputdirectory,outputdirectory,dataname,cut):

   #Read file 
   filelist       = glob.glob(inputdirectory+"/"+dataname+"/*.csv")
   outputfilename = outputdirectory+"/"+dataname+".txt"
   if len(filelist)>1: print "[WARNING] More than two files in %s"%dataname

   #Format [id,theoretical,measured]
   t_list = []
   b_list = []
   l_list = []
   r_list = []
   #Read file lines
   with open(filelist[0], "r") as my_input_file:
       for line in my_input_file:
           line = line.split(",", 8)
           if 'top' in line:         
               t_list.append([" ".join(line[0]), round( float(line[4]), 3) , round( float(line[6]), 3) ] )
           if 'bot' in line:         
               b_list.append([" ".join(line[0]), round( float(line[4]), 3) , round( float(line[6]), 3) ] )
           if 'left' in line:         
               l_list.append([" ".join(line[0]), round( float(line[4]), 3) , round( float(line[6]), 3) ] )
           if 'right' in line:         
               r_list.append([" ".join(line[0]), round( float(line[4]), 3) , round( float(line[6]), 3) ] )      
   with open(outputfilename, "w") as my_output_file:
       my_output_file.write("  {0:3}  {1:6}  {2:6}  {3:6}  {4:6}  {5:6}  {6:6}  {7:6}  {8:6} ".format("id","top_ms","top_th","bot_ms","bot_th", "lft_ms","lft_th","rgt_ms", "rgt_th")+ "\n")
       if cut==1:
              for k in range(0, len(t_list) ):
                  if (k % 2) == 1:
                     my_output_file.write("  {0:3}".format(str(k) ) )
                     my_output_file.write("  {0:6}  {1:6}".format(str(t_list[k][1]), str(t_list[k][2]) ))
                     my_output_file.write("  {0:6}  {1:6}".format(str(b_list[k][1]), str(b_list[k][2]) ))           
                     my_output_file.write("  {0:6}  {1:6}".format(str(l_list[k][1]), str(l_list[k][2]) ))   
                     my_output_file.write("  {0:6}  {1:6}".format(str(r_list[k][1]), str(r_list[k][2]) )+ "\n")
       else:
              for k in range(0, len(t_list) ):
                     my_output_file.write("  {0:3}".format(str(k) ) )
                     my_output_file.write("  {0:6}  {1:6}".format(str(t_list[k][1]), str(t_list[k][2]) ))
                     my_output_file.write("  {0:6}  {1:6}".format(str(b_list[k][1]), str(b_list[k][2]) ))           
                     my_output_file.write("  {0:6}  {1:6}".format(str(l_list[k][1]), str(l_list[k][2]) ))   
                     my_output_file.write("  {0:6}  {1:6}".format(str(r_list[k][1]), str(r_list[k][2]) )+ "\n")
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
         row = map( float, words )
         apply( ntuple.Fill, row )
     outfile.Write()
     print('[INFO] File '+outputname+ ' successfully written')

#Get input/output information
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--config' ,  dest='cfgfile',  help='Name of config file',  required = True)
parser.add_argument('--tag'    ,  dest='tag'    ,  help='Name of the default algo folder (e.g. Default)',  required = True)
args            = parser.parse_args()
configfilename  = args.cfgfile
tagname         = args.tag

print "[INFO] Reading configuration file . . ."
cfgparser = ConfigParser()
cfgparser.read('%s'%configfilename)
input_dir    = ast.literal_eval(cfgparser.get("processedconfiguration","input_dir"))
print "    -The input  directory:"
print "      *",input_dir
output_dir   = ast.literal_eval(cfgparser.get("processedconfiguration","output_dir"))
print "    -The output directory:"
print "      *",output_dir
datas      = ast.literal_eval(cfgparser.get("processedconfiguration","datas"))
print "    -The list of data files:"
for x in range(len(datas)): print "      *",datas[x]
datacuts   = ast.literal_eval(cfgparser.get("processedconfiguration","datacuts"))
os.system("mkdir ntuples")
os.system("mkdir ntuples/%s"%tagname)

for k in range( 0,len(datas)):
    print "[INFO] Reading %s"%datas[k]
    CSVReader(input_dir+"/"+tagname,output_dir+"/"+tagname,datas[k],datacuts[k])

for k in range( 0,len(datas)):
    print "[INFO] Ntuplizing %s"%datas[k]  
    MakeNtuple(output_dir+"/"+tagname,output_dir+"/"+tagname,datas[k])


