#!/usr/bin/env python

'''  
    jframepull.py
    
    
    Created by Jeannie Yeung on 27/11/12.
    Copyright (c) 2012 Park Road Post Production. All rights reserved.
'''


# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import os
import string
import math
import re
import sys
import shutil
import time
import subprocess
from multiprocessing import Process

__VERSION__ = 2.1


def puller():
    print '\nHey Dudes, this is script to pull sequences of chosen frames into separate folders...'
    print
        
    # Ask for user input of source sequence folder path
    sequencepath = raw_input("Please enter Path of the folder containing the source sequence: ").strip()
    print "You have entered: ", sequencepath + '\n'
    
    dstpath = raw_input("Please enter the destination path for the sequences of pulled out frames: ").strip()
    print "You have entered: ", dstpath + '\n'

    firstframe = getFirstFrame()
    endframe = getEndFrame()
    print
    padding = getPadding()
    
    print '\nPlease wait while the chosen files are being copied...'
    
    wantedcount = 0
    
    for root, dirs, frames in os.walk(sequencepath):
        frames.sort()
        
        for frame in frames:
            #framenamelist = frame.split('.')
            #currentframe = int(framenamelist[1])
            #rangefolderpath = os.path.join(dstpath, framenamelist[0]) + '_' + str(firstframe).zfill(6) + '-' + str(endframe).zfill(6)
        
            framename, framext = os.path.splitext(frame)
            match = re.search('(.*?)([0-9]{%d})$' % padding, framename)
            try:
                currentframe = int(match.group(2))
            except AttributeError, sequenceerr:
                print 'ERROR: ' + str(sequenceerr) + '\n'
                print 'Perhaps theres a file without a frame number in the source folder? Double check but the frame pull should have worked anyway.\n'

            if match.group(1) == '':
                head, tail = os.path.split(sequencepath)
                rangefoldername = tail + '_'
            else:
                rangefoldername = match.group(1)

            rangefolderpath = os.path.join(dstpath, rangefoldername) + str(firstframe).zfill(padding) + '-' + str(endframe).zfill(padding)
            
            if currentframe == firstframe:
                try:
                    os.makedirs(rangefolderpath)
                except Exception, mkdirerr:
                    print '\nPerhaps the folder is already there? ERROR: ' + str(mkdirerr) + '\n'
                    print '\nTry again. Quitting Script... Laterz!\n'
                    sys.exit(1)
                shutil.copy2(os.path.join(root, frame), rangefolderpath)
                print os.path.join(rangefolderpath, frame)
                wantedcount += 1
            elif currentframe > firstframe and currentframe < endframe:
                shutil.copy2(os.path.join(root, frame), rangefolderpath)
                print os.path.join(rangefolderpath, frame)
                wantedcount += 1
            elif currentframe == endframe:
                shutil.copy2(os.path.join(root, frame), rangefolderpath)
                print os.path.join(rangefolderpath, frame)
                wantedcount += 1
                print '\nDone. There should be %d frames in the new pulled out sequence folder, please check.' % wantedcount
                #print '\nQuitting Script... Laterz!\n'

                    
    # Ask the user if they want to tar the pulled out frames
    tarchoice = raw_input("Would you like to tar these pulled out frames? (y/n) ").strip()
    print
    if tarchoice == 'y' or tarchoice == 'Y':
        tarpath = raw_input("Please enter the destination path for the tar file: ").strip()
        print "You have entered: ", tarpath + '\n'

        tarScript = """
            cd $0
            cd ..
            foldername=`basename $0`
            tarfile=$1/$foldername.tar
            find -s $foldername \( ! -regex '.*/\..*' \) -type f > /tmp/tarframepulllist.txt
            gtar -cv -b 2048 -f $tarfile -T /tmp/tarframepulllist.txt
            
            echo ""
            """
        framestar = subprocess.Popen(['sh', '-c', tarScript, rangefolderpath, tarpath], stderr = subprocess.PIPE)
        framestar.wait()
        tarout, tarerr = framestar.communicate()

        if tarerr != '':
            print "An error has been caught during the tar:"
            print err
            print
            print "Please delete and re-tar normally with jstar_v3."
            print "Quitting Script... Laterz!\n"
            sys.exit(1)
        else:
            print
            print "Tar file is now ready for you, remember to delete the pulled out copy of frames if not needed."
            print "Quitting Script... Laterz!\n"
    else:
        print "Tar option has NOT been selected, enjoy the new frame sequence."
        print "Quitting Script... Laterz!\n"



    
def getFirstFrame():
    firstframe = raw_input("First frame number (incl): ").strip()
    try:
        return int(firstframe)
    except Exception, err:
        print '\nAre you sure you entered a number? Please see error printed below and try again.'
        print str(err) + '\n'
        getFirstFrame()
        

def getEndFrame():
    endframe = raw_input("End frame number (incl): ").strip()
    try:
        return int(endframe)
    except Exception, err:
        print '\nAre you sure you entered a number? Please see error printed below and try again.'
        print str(err) + '\n'
        getEndFrame()


def getPadding():
    padding = raw_input("Number of digits in frame name (padding): ").strip()
    try:
        return int(padding)
    except Exception, err:
        print '\nAre you sure you entered a number? Please see error printed below and try again.'
        print str(err) + '\n'
        getPadding()



if __name__ == '__main__':
	puller()

