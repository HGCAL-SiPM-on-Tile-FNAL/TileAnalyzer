import argparse
import sys, string
from ROOT import TFile, TNtuple

def CSVReader(inputfilename):
   outputfilename = inputfilename.replace(".csv", ".txt")
   #Format [id,theoretical,measured]
   t_list = []
   b_list = []
   l_list = []
   r_list = []
   #Read file lines
   with open(inputfilename, "r") as my_input_file:
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
       for k in range(0, len(t_list) ):
           my_output_file.write("  {0:3}".format(str(k) ) )
           my_output_file.write("  {0:6}  {1:6}".format(str(t_list[k][1]), str(t_list[k][2]) ))
           my_output_file.write("  {0:6}  {1:6}".format(str(b_list[k][1]), str(b_list[k][2]) ))           
           my_output_file.write("  {0:6}  {1:6}".format(str(l_list[k][1]), str(l_list[k][2]) ))   
           my_output_file.write("  {0:6}  {1:6}".format(str(r_list[k][1]), str(r_list[k][2]) )+ "\n")
       print('[INFO] File '+outputfilename+ ' successfully written')

def MakeNtuple(inputfilename):
     inputname  = inputfilename.replace(".csv", ".txt")
     outputname = inputfilename.replace(".csv", ".root")
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
parser.add_argument('--inputfile' ,  dest='inputfile',   help='Name of input file',  required = True)
args            = parser.parse_args()
inputfilename   = args.inputfile

#Run the reader
CSVReader(inputfilename)
MakeNtuple(inputfilename)