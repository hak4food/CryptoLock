#This code was written by Roland Smith 
#licensed under the Creative Commons Attribution 3.0 Unported License
#http://rsmith.home.xs4all.nl/miscellaneous/filtering-a-sound-recording.html

#Bryan Gonzalez Modified the code to fit the needs of CPSC597 Project. 
#This was intented for educational purposes.

import wave
import numpy as np
import sys

#inputs argv 1 as input file.
wr = wave.open(sys.argv[1], 'r')

# Parameters are read from the input file. 
par = list(wr.getparams()) 
# This file is stereo, 2 bytes/sample, 44.1 kHz.
par[3] = 0 # The number of samples will be set by writeframes.

# Open the output file
#outf = 'filter_'+str(sys.argv[1])
outf = str(sys.argv[2])
print('Processing complete', outf)
ww = wave.open(outf, 'w')

ww.setparams(tuple(par)) # Use the same parameters as the input file.

lowpass  = 600 #318   #21 Remove lower frequencies.
highpass = 7000#9000 # Remove higher frequencies.

sz = wr.getframerate() # Read and process 1 second at a time.
c = int(wr.getnframes()/sz) # whole file
for num in range(c):
    #print('Processing {}/{} s'.format(num+1, c))
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2] # left and right channel
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
    lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter
    lf[55:66], rf[55:66] = 0, 0 # line noise
    lf[highpass:], rf[highpass:] = 0,0 # high pass filter
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
    ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
    ww.writeframes(ns.tostring())

#Close the read file.
#Close the files.
wr.close()
ww.close()
