#!/usr/bin/env python

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

        print frames

if __name__ == '__main__':
	puller()