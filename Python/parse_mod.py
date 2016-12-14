# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 23:21:55 2016
Modified on Thu Dec 08 01:15:42 2016
@author: Teyvon

This file will plot the data of a csv file onto a graph
"""
#import all the goodies
#from matplotlib import pyplot as ppt
import argparse


def p():
    #initialize
    tcoor = []
    xcoor = []
    ycoor = []
    zcoor = [] 
    defaultname = 'FunTest.csv'  
    #defaultname = 'eulerorienttest2.csv'
    #defaultname = 'sample_motion.csv'
    #run = 0
    
    #def parse():
    
    #define argument parser
    parser = argparse.ArgumentParser()
    
    #Add all those argumments to out parser
    parser.add_argument('--filename', help = 'This is the name of the file you want to parse', action = 'store')
    
    #Start the fight
    arguments = parser.parse_args()     #define the argument function as the parser
    
    #Use the Arguments
    if arguments.filename == None:      #Test for an existing file or use default
        filename = defaultname
    else:
        filename = arguments.filename
    #read the default CSV file
    print ("loaded filename about to begin reading")
    #------------------Read and more----------------------
    try:
        with open(filename, 'r') as plt_data:       #starts with block to open the file
            data = plt_data.readlines()             #read the data in the csv file
    except IOError:
        print('File ' + filename + ' not found bruh') #Print error message for missing file
    else:
        for item in data:                      #and close the file.
            current_item = item.split(',')         #splits at commas for each line
            try:
                curr_t = float(current_item[0])
                curr_x = float(current_item[1])
                curr_y = float(current_item[2])
                curr_z = float(current_item[3])
            except ValueError: #if data is not able to become a float its no good
                print ('This item"' + current_item[0] + ', ' + current_item[1] + ', ' + current_item[2] + ', ' + current_item[3].rstrip('\n\r') + '" is not welcome here.')
            else:
    #-------------------plot stuff-----------------------
                tcoor.append(curr_t) #add the current value to the t array
                xcoor.append(curr_x) #add the current value to the x array
                ycoor.append(curr_y) #add the current value to the y array
                zcoor.append(curr_z) #add the current value to the z array
         
        print ("parsed but not returned yet")        
        return([tcoor,xcoor,ycoor,zcoor])
