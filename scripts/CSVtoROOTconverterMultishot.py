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
import time

def DirectoryFileReader(inputdirectory,outputdirectory,dataname,datasel,npoints):
  #Read file
  filelist      = []
  for k in range(1,int(npoints)+1):
        file  = glob.glob(inputdirectory+"/"+dataname+"/point_%i/"%k+datasel+"/*.csv")
        info  = [] 
        with open(file[0], "r") as my_input_file:
          kinfo = []
          for line in my_input_file:
              if 'nid' in line:
                  line = line.split(",", 2)        
                  kinfo.append(int(line[1]))
              if 'nx' in line:         
                  line = line.split(",", 2)    
                  kinfo.append(float(line[1]))
              if 'ny' in line:         
                  line = line.split(",", 2)    
                  kinfo.append(float(line[1]))
              if len(kinfo)==3:
                  info.append(kinfo)
                  kinfo=[]
        info = sorted(info, key=lambda x: x[0], reverse=False)
        c1    = glob.glob(inputdirectory+"/"+dataname+"/point_%i/"%k+datasel+"/*_1_contour.jpg")
        c2    = glob.glob(inputdirectory+"/"+dataname+"/point_%i/"%k+datasel+"/*_2_contour.jpg")
        c3    = glob.glob(inputdirectory+"/"+dataname+"/point_%i/"%k+datasel+"/*_3_contour.jpg")
        c4    = glob.glob(inputdirectory+"/"+dataname+"/point_%i/"%k+datasel+"/*_4_contour.jpg")
        c = [c1[0],c2[0],c3[0],c4[0]]
        filelist.append([[info[0],c[0]],[info[1],c[1]],[info[2],c[2]],[info[3],c[3]]]) 
  return filelist

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

def convertcameracenter(coordinates,ncols,nrows):
    k = 0.04589621286 #mm per pixel
    #print "[INFO] Converting corner information"
    xp = coordinates[0]-(ncols/2)
    yp = coordinates[1]-(nrows/2)
    cx = round(xp*k,3)
    cy = round(yp*-k,3)
    return cx,cy

def filtercircle(inputpic):
    img = inputpic.copy()
    nrows, ncols, rgb = img.shape
    cx     = ncols/2
    cy     = nrows/2
    r      = nrows/2
    for i in range(0, nrows):         
      for j in range(0, ncols):
           distance = math.sqrt(  (j-cx)*(j-cx) + (i-cy)*(i-cy))
           if distance < 0.85*r and distance>0.10*r: continue
           for k in range(0, rgb): img[i,j,k] = 0
    return img

def filterhorizontalandvertical(inputpic,res,tag):
    #print "[INFO] Pixel analysis on corner %s"%tag
    imgh = inputpic.copy()
    imgv = inputpic.copy()
    nrows, ncols, rgb = imgh.shape
    w_h_xmin  = 0
    w_h_xmax  = 0
    w_h_ymax  = 0
    w_h_ymin  = 0
    w_v_xmin  = 0
    w_v_xmax  = 0
    w_v_ymax  = 0
    w_v_ymin  = 0
    pixels_xy = []
    #Find all white pixel in x-axis
    for i in range(0, nrows):         
      for j in range(0, ncols):         
           if imgh[i,j,0] != 0: 
              pixels_xy.append([j,i])
    pixels_xy_byx= sorted(pixels_xy, key=lambda x: x[0], reverse=True)
    pixels_xy_byy= sorted(pixels_xy, key=lambda x: x[1], reverse=True)
    #Find key points for edge recognition
    minx = pixels_xy_byx[len(pixels_xy_byx)-1]
    maxx = pixels_xy_byx[0]
    miny = pixels_xy_byy[len(pixels_xy_byy)-1]
    maxy = pixels_xy_byy[0]
    #Filter windows 
    if minx[0]<ncols*0.4 and maxy[1]>nrows*0.6: 
        #Windows for horizontal
        w_h_xmin = minx[0]
        w_h_xmax = maxx[0]
        w_h_ymax = minx[1]+res
        w_h_ymin = minx[1]-res
        #Windows for vertical
        w_v_xmin = maxx[0]-res
        w_v_xmax = maxx[0]+res
        w_v_ymax = maxy[1]
        w_v_ymin = miny[1]
    elif maxx[0]>ncols*0.6 and maxy[1]>nrows*0.6:
        #Windows for horizontal
        w_h_xmin = minx[0]
        w_h_xmax = maxx[0]
        w_h_ymax = maxx[1]+res
        w_h_ymin = maxx[1]-res
        #Windows for vertical
        w_v_xmin = minx[0]-res
        w_v_xmax = minx[0]+res
        w_v_ymax = maxy[1]
        w_v_ymin = miny[1]        
    elif minx[0]<ncols*0.4 and miny[1]<nrows*0.4: 
        #Windows for horizontal
        w_h_xmin = minx[0]
        w_h_xmax = maxx[0]
        w_h_ymax = minx[1]+res
        w_h_ymin = minx[1]-res
        #Windows for vertical
        w_v_xmin = maxx[0]-res
        w_v_xmax = maxx[0]+res
        w_v_ymax = maxy[1]
        w_v_ymin = miny[1]
    elif maxx[0]>ncols*0.6 and miny[1]<nrows*0.4:
        #Windows for horizontal
        w_h_xmin = minx[0]
        w_h_xmax = maxx[0]
        w_h_ymax = maxx[1]+res
        w_h_ymin = maxx[1]-res
        #Windows for vertical
        w_v_xmin = minx[0]-res
        w_v_xmax = minx[0]+res
        w_v_ymax = maxy[1]
        w_v_ymin = miny[1]        
    else:
        print "[WARNING] Exceptional case: Not covered by algo, so filter will not make sense"
    #Filter only horizontal
    for i in range(0, nrows):         
      for j in range(0, ncols):
               if i>=w_h_ymin and i<=w_h_ymax and j>=w_h_xmin and j<=w_h_xmax: continue
               for k in range(0, rgb): imgh[i,j,k] = 0
    #Filter only vertical
    for i in range(0, nrows):         
      for j in range(0, ncols):      
               if i>=w_v_ymin and i<=w_v_ymax and j>=w_v_xmin and j<=w_v_xmax: continue
               for k in range(0, rgb): imgv[i,j,k] = 0
    return imgh,imgv

def findintersection(fit1,fit2,low,high):
    max_dk = high
    x = 0.0
    y = 0.0
    steps = (high - low)*10000 
    points = [ 0 + k*0.0001 for k in range(0,steps+1)]
    for k in points:
         k1 = fit1.Eval(k)
         k2 = fit2.Eval(k)
         if abs(k2-k1)<max_dk:
            max_dk = abs(k2-k1)
            x = k
            y = fit2.Eval(k)
    return float(x),float(y)

def makegraph(inputpic):
    img = inputpic.copy()
    nrows, ncols, rgb = img.shape
    pixels_xy = []
    #Find all white pixel in x-axis
    for i in range(0, nrows):         
      for j in range(0, ncols):         
           if img[i,j,0] != 0: 
              pixels_xy.append([j,i])
    #order them from low x to high x          
    pixels_xy = sorted(pixels_xy, key=lambda x: x[0], reverse=False)
    #Rotate points
    pixels_xy_rot =[]
    for i in range(0, len(pixels_xy)):
       a = float(pixels_xy[i][0])
       b = float(pixels_xy[i][1])
       ap= (a*math.cos(math.pi/4)) - (b*math.sin(math.pi/4))
       bp= (a*math.sin(math.pi/4)) + (b*math.cos(math.pi/4))
       pixels_xy_rot.append([ap,bp])
    pixels_xy_rot = sorted(pixels_xy_rot, key=lambda x: x[0], reverse=False)
    x, y = array( 'f' ), array( 'f' )
    for i in range(0, len(pixels_xy_rot)):
           x.append(pixels_xy_rot[i][0])
           y.append(pixels_xy_rot[i][1])    
    gr = TGraph( len(pixels_xy_rot), x, y )
    return gr

def makefits(inputh,inputv,tag):
    #Get points for fits
    nrows, ncols, rgb = inputh.shape
    gr1 = makegraph(inputh)
    gr2 = makegraph(inputv)
    #Get min/max for fit
    n_1    = gr1.GetN()      
    maxx_1 = gr1.GetX()[n_1-1]
    minx_1 = gr1.GetX()[0]
    n_2    = gr2.GetN()      
    maxx_2 = gr2.GetX()[n_2-1]
    minx_2 = gr2.GetX()[0]
    #Fit to graphs with linear function 
    gr1.Fit("pol1","RQ","",minx_1,maxx_1)
    gr2.Fit("pol1","RQ","",minx_2,maxx_2)
    #Find the intersection
    fit1 = gr1.GetFunction("pol1")
    fit2 = gr2.GetFunction("pol1")
    x,y  = findintersection(fit1,fit2,-ncols,ncols)

    a = (float(x)*math.cos(-math.pi/4)) - (float(y)*math.sin(-math.pi/4))
    b = (float(x)*math.sin(-math.pi/4)) + (float(y)*math.cos(-math.pi/4))

    return [a,b], [fit1.GetParameter(0),fit1.GetParameter(1)], [fit2.GetParameter(0),fit2.GetParameter(1)]

def multishotreconstruction(dataset):
    #Noozle position in extra shots 
    n_1 = [dataset[0][0][1],dataset[0][0][2]]
    n_2 = [dataset[1][0][1],dataset[1][0][2]]
    n_3 = [dataset[2][0][1],dataset[2][0][2]]
    n_4 = [dataset[3][0][1],dataset[3][0][2]]
    #original contours (in RGB)
    img_original_1   = cv2.imread(dataset[0][1])
    img_original_2   = cv2.imread(dataset[1][1])
    img_original_3   = cv2.imread(dataset[2][1])
    img_original_4   = cv2.imread(dataset[3][1])
    #filter circle from contours (in RGB)
    img_nocircle_1   = filtercircle(img_original_1)
    img_nocircle_2   = filtercircle(img_original_2)
    img_nocircle_3   = filtercircle(img_original_3)
    img_nocircle_4   = filtercircle(img_original_4)
    #filter horizontal and vertical lines (in RGB)
    img_horizontal_1,img_vertical_1 = filterhorizontalandvertical(img_nocircle_1,20,"1")
    img_horizontal_2,img_vertical_2 = filterhorizontalandvertical(img_nocircle_2,20,"2")
    img_horizontal_3,img_vertical_3 = filterhorizontalandvertical(img_nocircle_3,20,"3")
    img_horizontal_4,img_vertical_4 = filterhorizontalandvertical(img_nocircle_4,20,"4")
    #fit points
    xy_1,fit1_1,fit2_1 = makefits(img_horizontal_1,img_vertical_1,"1")
    xy_2,fit1_2,fit2_2 = makefits(img_horizontal_2,img_vertical_2,"2")
    xy_3,fit1_3,fit2_3 = makefits(img_horizontal_3,img_vertical_3,"3")
    xy_4,fit1_4,fit2_4 = makefits(img_horizontal_4,img_vertical_4,"4")
    #Convert fitted corners in mm (w.r.t to camera center)
    c_1 = convertcameracenter(xy_1,img_original_1.shape[1],img_original_1.shape[0])
    c_2 = convertcameracenter(xy_2,img_original_2.shape[1],img_original_2.shape[0])
    c_3 = convertcameracenter(xy_3,img_original_3.shape[1],img_original_3.shape[0])
    c_4 = convertcameracenter(xy_4,img_original_4.shape[1],img_original_4.shape[0])
    #Convert to global coordinates
    p_1 = [  n_3[0] + c_1[0],  n_3[1] + c_1[1] ]
    p_2 = [  n_4[0] + c_2[0],  n_4[1] + c_2[1] ]
    p_3 = [  n_1[0] + c_3[0],  n_1[1] + c_3[1] ]
    p_4 = [  n_2[0] + c_4[0],  n_2[1] + c_4[1] ]
    #Compute tile dimension
    top = math.sqrt(  (p_1[0]-p_2[0])*(p_1[0]-p_2[0]) + (p_1[1]-p_2[1])*(p_1[1]-p_2[1]) )
    lef = math.sqrt(  (p_2[0]-p_3[0])*(p_2[0]-p_3[0]) + (p_2[1]-p_3[1])*(p_2[1]-p_3[1]) )
    bot = math.sqrt(  (p_3[0]-p_4[0])*(p_3[0]-p_4[0]) + (p_3[1]-p_4[1])*(p_3[1]-p_4[1]) )
    rig = math.sqrt(  (p_4[0]-p_1[0])*(p_4[0]-p_1[0]) + (p_4[1]-p_1[1])*(p_4[1]-p_1[1]) )
    #return measurements
    return [top,bot,lef,rig]

def RunMultishotReconstruction(inputdirectory,outputdirectory,dataname,datasel,npoints,expected):
    print "[INFO] Reading %s"%dataname
    outputfilename = outputdirectory+"/"+dataname+".txt"
    dataset =  DirectoryFileReader(inputdirectory,outputdirectory,dataname,datasel,npoints)
    list_tiledimension = []
    for j in range(0,npoints):
         tiledimensions = multishotreconstruction(dataset[j])
         list_tiledimension.append(tiledimensions)
         print tiledimensions
    with open(outputfilename, "w") as my_output_file:
       my_output_file.write("  {0:3}  {1:6}  {2:6}  {3:6}  {4:6}  {5:6}  {6:6}  {7:6}  {8:6} ".format("id","top_ms","top_th","bot_ms","bot_th", "lft_ms","lft_th","rgt_ms", "rgt_th")+ "\n")
       for k in range(0, len(list_tiledimension) ):
                     my_output_file.write("  {0:3}".format(str(k) ) )
                     my_output_file.write("  {0:6}  {1:6}".format(str(list_tiledimension[k][0]), str(expected[0]) ))
                     my_output_file.write("  {0:6}  {1:6}".format(str(list_tiledimension[k][1]), str(expected[1]) ))           
                     my_output_file.write("  {0:6}  {1:6}".format(str(list_tiledimension[k][2]), str(expected[2]) ))   
                     my_output_file.write("  {0:6}  {1:6}".format(str(list_tiledimension[k][3]), str(expected[3]) )+ "\n")
       print('[INFO] File '+outputfilename+ ' successfully written')

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
datasel    = ast.literal_eval(cfgparser.get("processedconfiguration","datasel"))
npoints    = ast.literal_eval(cfgparser.get("processedconfiguration","npoints"))
expected   = ast.literal_eval(cfgparser.get("processedconfiguration","expected"))
print "    -The list of data features"
print "      * Expected dimension:",expected
print "      * Selection folder:"  ,datasel
print "      * # points :",npoints
os.system("mkdir ntuples")
os.system("mkdir ntuples/%s"%tagname)


#Create pool of processes   
starttime = time.time()
processes = []
threadNumber=1  # datas entries <= n <= 8
listNumber = 0
skimFileListOfList = [ [] for i in range(threadNumber)]
for fileName in datas:
    skimFileListOfList[listNumber].append(fileName)
    listNumber = listNumber + 1
    if listNumber >= 1:  # datas entries <= n <= 8
      listNumber = 0
for i in range(threadNumber):
  dataname = skimFileListOfList[i][0]
  p = mp.Process(target=RunMultishotReconstruction, args=(input_dir+"/"+tagname,output_dir+"/"+tagname,dataname, datasel, npoints, expected))
  processes.append(p)
  p.start()
for process in processes:
  process.join()

for k in range( 0,len(datas)):
    print "[INFO] Ntuplizing %s"%datas[k]  
    MakeNtuple(output_dir+"/"+tagname,output_dir+"/"+tagname,datas[k])

print '[INFO] Running multuthread took {} seconds'.format(time.time() - starttime)


