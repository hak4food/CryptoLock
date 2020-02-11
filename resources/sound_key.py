import sys
import os
import math
from numpy import linspace
from scipy.io.wavfile import read
from scipy import signal
from numpy import *
import platform
from matplotlib import *
import matplotlib.pyplot as plt
from math import atan2,log
from numpy import zeros,argmax,mean
from scipy.fftpack import fft 
from scipy.fftpack import rfft
from pylab import *

#####################
#Class function
#####################
def roundup100(x):
 y = int(math.ceil(x/500.0)) *500
 #print(y)
 return y
 
def roundupT(x):
 y = int(math.ceil(x/0.5)) *0.5
 #print(y)
 return y
                 
class FFT_audio:

    def __init__(self,a,b,imr):
        self.a=a
        self.b=b
        self.imr=imr
        pass
        
    def fft_data(self):
        num=len(self.b)

        noct=int(log(num)/log(2))
        
        if(noct>20):
            noct=20

        num_fft=2**noct

        bb=self.b[0:num_fft]
        
        if(self.imr==1):
            bb=bb-mean(bb)

        dur_fft=self.a[num_fft-1]-self.a[0]

        df=1/dur_fft

        z =fft(bb)
	
        k= numpy.fft.fftfreq(len(bb))[range(0,num_fft)]
        freq_pwr  = 10*log10(1e-20+abs(rfft(bb,num_fft)))
        #fo = open("power.txt","a")
        #fo.write(str(freq_pwr))	
        #fo.write(' ')	
        #fo.close()	
                    		
        nhalf=num_fft/2

        zz=zeros(nhalf,'f')
        ff=zeros(nhalf,'f')
        ph=zeros(nhalf,'f')

        freq=zeros(num_fft,'f')

        z/=float(num_fft)
	
        h=int(num_fft)
	
        for k in range(0,int(num_fft)):
            freq[k]=k*df
    
        ff=freq[0:nhalf]
    
        for k in range(0,int(nhalf)):    

            if(k > 0):			 
                zz[k]=2.*abs(z[k])
            else:    
                zz[k]= abs(z[k])

            ph[k]=atan2(z.real[k],z.imag[k])
  

        idx = argmax(abs(zz))        
 
        return idx,freq,ff,z,zz,ph,nhalf,df,num_fft    
   
sumValueMean = 0
sumValueFreq = 0
#####################
#open files function
#####################
#file_path = sys.argv[1]
for x in range (1,6):
 file_path = 'resources/filter_'+ str(x) + '.wav'
 rate,data=read(file_path)
 nad=data.ndim
 #print(file_path)

 if(nad==2):
     np=data.shape[0]
     nr=data.shape[1]

 dt=1/float(rate)

 t=linspace(0,(np-1)*dt,np)

 #####################
 #Process data 
 #####################
 imr=1 # mean removal
 idx1,freq1,ff1,z1,zz1,ph1,nhalf1,df1,num_fft1=FFT_audio(t,data[:,0],imr).fft_data()  
 idx2,freq2,ff2,z2,zz2,ph2,nhalf2,df2,num_fft2=FFT_audio(t,data[:,1],imr).fft_data()

 q1= data[:,0]
 q2= data[:,1]

 Pxx1, freqs1, bins1, im1 = specgram(q1,NFFT=1024, Fs=44100)
 #print ('PxxL = ')
 #print (Pxx)	 
 xxxx1= mean(Pxx1)
 sumValueMean += xxxx1
 #print ("Mean equals Ch1= %8.6g "% (xxxx1) )  
 #print (xxxx1)
 Pxx2, freqs2, bins2, im2 = specgram(q2,NFFT=1024, Fs=44100)
 #print ('PxxR = ')
 #print (Pxx)
 xxxx2= mean(Pxx2)
 sumValueMean += xxxx2
 #print ("Mean equals Ch2= %8.6g "% (xxxx2) ) 
 #print (xxxx2)	

 #print ("Ch 1  Peak Amp at Freq=%8.4g Hz  " %(ff1[idx1]))     
 #print ("Ch 2  Peak Amp at Freq=%8.4g Hz  " %(ff2[idx2]))
 sumValueFreq += ff1[idx1]
 sumValueFreq += ff1[idx1]
 
avgVal = sumValueMean/10
avgValFreq = sumValueFreq /10
#print(avgVal)
#print(avgValFreq)
a = roundupT(avgVal)
b = roundup100(avgValFreq)

tmp = str(a) + str(b)
print (tmp)
