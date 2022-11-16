#Here do code for making folders for analysis
import argparse
import sys, string
import os
import argparse
import ast
import glob
import math
from  ConfigParser import *
from ROOT import TFile, TNtuple,TGraph
import cv2 
import numpy as np
from array import array
import multiprocessing as mp

def DirectoryFileMaker(inputdirectory,outputdirectory,dataname):
  #Read files
  csvfile  = glob.glob(inputdirectory+"/"+dataname+"/*.csv")
  c1       = glob.glob(inputdirectory+"/"+dataname+"/*_1_contour.jpg")
  c2       = glob.glob(inputdirectory+"/"+dataname+"/*_2_contour.jpg")
  c3       = glob.glob(inputdirectory+"/"+dataname+"/*_3_contour.jpg")
  c4       = glob.glob(inputdirectory+"/"+dataname+"/*_4_contour.jpg")

  #Order alphanumerically
  csvfile.sort()
  c1.sort()
  c2.sort()
  c3.sort()
  c4.sort()

  #Make directories
  npoints = len(csvfile)/2
  ninputs = len(csvfile)
  for k in range(1,npoints+1): 
    os.system("mkdir %s/%s/point_%i"%(outputdirectory,dataname,k))
    os.system("mkdir %s/%s/point_%i/initial"%(outputdirectory,dataname,k))
    os.system("mkdir %s/%s/point_%i/final"%(outputdirectory,dataname,k))

  #Files to the new directories
  pi=1
  pf=1
  for k in range(0,ninputs):
    if (k % 2) == 0: 
      if pi <= npoints:
        os.system("cp -r %s %s/%s/point_%i/initial/"%(csvfile[k],outputdirectory,dataname,pi))
        os.system("cp -r %s %s/%s/point_%i/initial/"%(c1[k]     ,outputdirectory,dataname,pi))
        os.system("cp -r %s %s/%s/point_%i/initial/"%(c2[k]     ,outputdirectory,dataname,pi))
        os.system("cp -r %s %s/%s/point_%i/initial/"%(c3[k]     ,outputdirectory,dataname,pi))
        os.system("cp -r %s %s/%s/point_%i/initial/"%(c4[k]     ,outputdirectory,dataname,pi))
      pi+=1
    else: 
      if pf <= npoints: 
        os.system("cp -r %s %s/%s/point_%i/final/"%(csvfile[k],outputdirectory,dataname,pf))
        os.system("cp -r %s %s/%s/point_%i/final/"%(c1[k]     ,outputdirectory,dataname,pf))
        os.system("cp -r %s %s/%s/point_%i/final/"%(c2[k]     ,outputdirectory,dataname,pf))
        os.system("cp -r %s %s/%s/point_%i/final/"%(c3[k]     ,outputdirectory,dataname,pf))
        os.system("cp -r %s %s/%s/point_%i/final/"%(c4[k]     ,outputdirectory,dataname,pf))
      pf+=1

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
input_dir    = ast.literal_eval(cfgparser.get("rawconfiguration","input_dir"))
print "    -The input  directory:"
print "      *",input_dir
output_dir   = ast.literal_eval(cfgparser.get("rawconfiguration","output_dir"))
print "    -The output directory:"
print "      *",output_dir
datas       = ast.literal_eval(cfgparser.get("rawconfiguration","datas"))
print "    -The list of data files:"
for x in range(len(datas)): print "      *",datas[x]
isMultishot = ast.literal_eval(cfgparser.get("rawconfiguration","multishot"))

os.system("mkdir %s"%output_dir)
os.system("mkdir %s/%s"%(output_dir,tagname))
if int(isMultishot)==1:
  for dataname in datas:
     os.system("mkdir %s/%s/%s"%(output_dir,tagname,dataname) )
     DirectoryFileMaker(input_dir,output_dir+"/%s"%tagname,dataname)
else:
  for dataname in datas:
     os.system("cp -r %s/%s %s/%s/%s"%(input_dir, dataname, output_dir,tagname,dataname) )