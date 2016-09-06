# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:28:06 2016

@author: jmeza
"""

''' 
This is the final wavelength calibration code that implements the 
grating equation to calculate the wavelength dispersion.
The input should just be the name of a comparison lamp, taken from argv. 
The function depend on some hard coded data, "WaveList" and "Parameters" which 
are project spesific. 

Use: 
>>> python WaveCal.py lamp_spec.ms.fits

:INPUTS:
       lamp_spec.ms.fits: string, 1D Fe lamp spectrum 

:OPTIONAL:
       ZZCeti_spectrum.ms.fits: string, parameters written to header of this image if supplied when prompted

:OUTPUTS:
       wtFe*fits: lamp spectrum with wavelength calibration parameters written to header

       w*fits: ZZ Ceti spectrum with wavelength calibration parameters written to header

       wavecal_ZZCETINAME_DATE.txt: saved parameters for diagnostics. ZZCETINAME is name of the ZZ Ceti spectrum supplied. DATE is the current date and time. Columns are: fitted wavelengths, residuals, wavelengths, flux, lambdas fit,  wavelengths, sky flux, fit to line for recentering

To do:
- Add method to reject lines after refitting


'''
# ==========================================================================
# Imports # ================================================================
# ==========================================================================

import ReduceSpec_tools as rt 
import numpy as np
import pyfits as pf
import scipy.signal as sg
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, fsolve
import mpfit
import datetime

# ==========================================================================
# Data # ===================================================================
# ==========================================================================

# Grating Eq Parameters  
# Parameters= [fr, fd, fl, zPnt] 
# fr= fringe density of grating 
# fa= grat. ang fudge
# fd= camera angle correction factor 
# fl = focal lenght 
# zPnt= Zero point pixel offset

# As close to the red set up as I currently have (930_20_40)
Param_930_20_40= [92.668, 0.973, 377190., 1859.]
# As close to the blue  set up as I currently have (930_12_24)
Param_930_12_24= [92.517, 0.962, 377190., 1836.]

# ==========================================================================

# Pixel-Wavelenght List # 
# WaveList== array (2, number of lines) 
# WaveList[0]== pixels
# WaveList[1]== Wavelenghts
# As close to the red setup (20_35.2) as I currently have # 
'''
These are the original lists. Below we have selected the lines that can consistently be fit by a Gaussian. These are kept for archival purposes.
WaveList_Fe_930_20_40= np.array([ [1155.1, 102.964, 142.88, 276.362, 438.35, 532.819, 
                                631.475, 755.5, 798.185, 831.719, 1062.43, 1086.89, 
                                1249.02, 1316.94, 1475.64, 1566.37, 1762.42, 
                                1910, 2053.55, 2072.75, 2168.64, 2179.14, 
                                2271.52, 2318.23, 2347.65, 2370.04, 2417.91, 
                                2645.82, 2672.71, 3385.8, 3562.11, 3620.55, 
                                3765.62, 3913.77, 3935.87, 4016.2, 4034.6], 
                                
                                [6043.223, 6466.5526, 6483.0825, 6538.112, 6604.8534, 
                                 6643.6976, 5875.618, 6684.2929, 6752.8335, 6766.6117, 
                                 6861.2688, 6871.2891, 6937.6642, 6965.4307, 
                                 7030.2514, 7067.2181, 7147.0416, 7206.9804, 
                                 7265.1724, 7272.9359, 7311.7159, 7316.005, 
                                 7353.293, 7372.1184, 7383.9805, 7392.9801, 
                                 7412.3368, 7503.8691, 7514.6518, 7798.5604, 
                                 7868.1946, 7891.075, 7948.1964, 8006.1567, 
                                 8014.7857, 8046.1169, 8053.3085] ])

# As close to the blue setup (12_24) as I currently have # 

WaveList_Fe_930_12_24= np.array([ [34.6852, 431.795, 451.264, 942.966, 1057.76, 
                                   1174.6, 1194.97, 1315.35, 1381.1, 1444.58, 
                                   1457.81, 1538.65, 1544.11, 1630.61, 1682.99, 
                                   1713.34, 1726.03, 1779.61, 1886.38, 1893.19, 
                                   1959.28, 1968.19, 1980.81, 2018.27, 2078.23, 
                                   2088.47, 2132.53, 2194.03, 2210.85, 2279.64, 
                                   2361.34, 2443.06, 2468.22, 2515.14, 2630.53, 
                                   2795.45, 2807.86, 2817.11, 2886.45, 2985.15, 
                                   3085.52, 3162.56, 3184.41, 3367.86, 3493.34, 
                                   3602.21, 3795.76, 3845.65, 3907.57], 
                                   
                                   [3561.0304, 3729.3087, 3737.1313, 3946.0971, 
                                    3994.7918, 4044.4179, 4052.9208, 4103.9121, 
                                    4131.7235, 4158.5905, 4164.1795, 4198.3036, 
                                    4200.6745, 4237.2198, 4259.3619, 4271.7593, 
                                    4277.5282, 4300.1008, 4345.168, 4348.064, 
                                    4375.9294, 4379.6668, 4385.0566, 4400.9863, 
                                    4426.0011, 4430.189, 4448.8792, 4474.7594, 
                                    4481.8107, 4510.7332, 4545.0519, 4579.3495, 
                                    4589.8978, 4609.5673, 4657.9012, 4726.8683, 
                                    4732.0532, 4735.9058, 4764.8646, 4806.0205, 
                                    4847.8095, 4879.8635, 4889.0422, 4965.0795, 
                                    5017.1628, 5062.0371, 5141.7827, 5162.2846, 
                                    5187.7462] ]) 
'''
WaveList_Fe_930_12_24= np.array([ [431.795, 1057.76, 1194.97, 1315.35, 
                                   1381.1, 1444.58, 1457.81, 1630.61, 
                                   1682.99, 1713.34, 1726.03, 1779.61, 
                                   1893.19, 2018.27, 2132.53, 2210.85, 
                                   2279.64, 2361.34, 2443.06, 2468.22, 
                                   2515.14, 2630.53, 2795.45, 2886.45, 
                                   2985.15, 3085.52, 3162.56, 3184.41, 
                                   3367.86, 3602.21, 3795.76, 3845.65, 
                                   3907.57], 
                                   
                                   [3729.3087, 3994.7918, 4052.9208, 4103.9121, 
                                    4131.7235, 4158.5905, 4164.1795, 4237.2198, 
                                    4259.3619, 4271.7593, 4277.5282, 4300.1008, 
                                    4348.064, 4400.9863, 4448.8792, 4481.8107, 
                                    4510.7332, 4545.0519, 4579.3495, 4589.8978, 
                                    4609.5673, 4657.9012, 4726.8683, 4764.8646, 
                                    4806.0205, 4847.8095, 4879.8635, 4889.0422, 
                                    4965.0795, 5062.0371, 5141.7827, 5162.2846, 
                                    5187.7462] ]) 

WaveList_Fe_930_20_40= np.array([ [1155.1, 102.964, 142.88, 276.362, 438.35, 
                                   532.819, 631.475, 755.5, 798.185, 831.719, 
                                   1062.43, 1086.89, 1249.02, 1316.94, 
                                   1475.64, 1762.42, 1910.0], 
                                
                                [6043.223, 6466.5526, 6483.0825, 6538.112, 6604.8534, 
                                 6643.6976, 5875.618, 6684.2929, 6752.8335, 6766.6117, 
                                 6861.2688, 6871.2891, 6937.6642, 6965.4307, 
                                 7030.2514, 7147.0416, 7206.9804] ])


# ==========================================================================
# Functions # ==============================================================
# ==========================================================================

def DispCalc(Pixels, alpha, theta, fr, fd, fl, zPnt):
    # This is the Grating Equation used to calculate the wavelenght of a pixel
    # based on the fitted parameters and angle set up.
    # Inputs: 
    # Pixels= Vector of Pixel Numbers
    # alpha=  of Grating Angle
    # aheta=  Camera Angle
    # fr= fringe density of grating
    # fd= Camera Angle Correction Factor
    # zPnt= Zero point pixel 
    Wavelengths= [] # Vector to store calculated wavelengths 
    for pix in Pixels:    
        beta = np.arctan( (pix-zPnt)*15./fl ) + (fd*theta*np.pi/180.) - (alpha*np.pi/180.) 
        wave = (10**6.)*( np.sin(beta) + np.sin(alpha*np.pi/180.) )/fr
        Wavelengths.append(wave)
    return Wavelengths
    
# ===========================================================================

def PixCalc(Wavelenghts, alpha, theta, fr, fd, fl, zPnt):
    # This is the Grating Equation used to calculate the pixel number of a for 
    # a certain wavelength based on the fitted parameters and angle set up.
    # Inputs: 
    # Wavelenght= Vector of Wavelengths in Angstrums
    # alpha=  Grating Angle
    # aheta=  Camera Angle
    # fr= fringe density of grating
    # fd= Camera Angle Correction Factor
    # zPnt= Zero point pixel 
    Pixels= [] # Vector to store calculated wavelengths 
    for wave in Wavelenghts:   
        beta = np.arcsin( ((wave*fr/1000000.0)) - np.sin(alpha*np.pi/180.) )
        pix = np.tan((beta + (alpha*np.pi/180.)) - (fd*theta*np.pi/180.)) * (fl/15.) + zPnt
        Pixels.append(pix)
    return Pixels

# ===========================================================================

def Gauss(x,a,c,w,b):
        # Define a Gousian Function # 
        # x= some value
        # a= amplitude, c= center, w=  RMS width. 
        # Output= y: gausian evaluated at x 
        y= a*np.exp( (-(x-c)**2.)/(2.*w**2.) ) + b
        return y   

# ===========================================================================

def CrossCorr(lamp_data):
    # This sunction takes a lamp spectra and cross corelates the data with 
    # Gaussian of RMS width= 1, amplitude= 1, peaked at each pixel. 
    # It reteturns a list of peak values.    
    nx= np.size(lamp_data); # Number of pixels
    X= np.arange(nx) # Vector of pixel values 
    Corr= np.zeros(nx) # Vector to store cross corrolated result 
    # Calculate Cross Correlation
    print ("\nCross Correlateing")
    for i in range(0,nx):
       G= [Gauss(X[n],1.,i,3.,0.) for n in range(0,nx)]
       Corr= Corr+ G*lamp_data;
    return Corr

# ===========================================================================

def PeakFind(data):
    print "\nFinding Peaks"
    widths= np.arange(1.,5.,.1)
    maybe= sg.find_peaks_cwt(data, widths)
    n= np.size(maybe)
    prob= []
    for i in range(0,n):
        if (maybe[i]-maybe[i-1])==1:
            prob.append( np.max([maybe[i],maybe[i-1]]) )
        else:
            prob.append(maybe[i])
    peaks_x= []
    peaks_y= []
    std= np.std(data)
    for p in prob:
        if data[p]>2.0*std:
            peaks_x.append(p)
            peaks_y.append(data[p])               
    return peaks_x, peaks_y
    
# ===========================================================================
    
def fit_Gauss(X,Y):
    a0= np.max(Y)/2.0
    c0= X[ np.argmax(Y) ]
    w0= 3.0*0.42
    b0= np.mean(Y)
    par, cov = curve_fit(Gauss, X, Y, p0 = [a0, c0 , w0, b0], maxfev= 1000)
    return par

# ===========================================================================

def find_peak_centers(peak_w, Wavelen, Counts):
    list_centers= []
    for w in peak_w:
        i= Wavelen.index(w) # index of peak_w with wavelengths list
        fit_data_w= Wavelen[i-9:i+9]
        fit_data_c= Counts[i-9:i+9]
        amp, cent, width, b= fit_Gauss(fit_data_w, fit_data_c)
        list_centers.append(cent)
        ## Plot the gaussian fit 
        X= np.arange(fit_data_w[0],fit_data_w[-1], (fit_data_w[-1]-fit_data_w[0])/50.0 )
        Y= [Gauss(x, amp, cent, width, b) for x in X]
        #plt.plot(fit_data_w, fit_data_c)
        #plt.hold('on')
        #plt.plot(X, Y, 'r--')
        #plt.axvline(cent)
        #plt.hold('off')
        #print cent
        #plt.show()
    return list_centers

# ===========================================================================

def onclick(event):
    global ix,iy
    ix, iy = event.xdata,event.ydata
    global coords
    ax.axvline(x=ix,color='k',linewidth='2')
    fig.canvas.draw()
    coords.append((ix,iy))

# ===========================================================================

def find_near(p, in_data):
    # find the index of the point in_data nearest point p. 
    near= min(in_data, key=lambda x:abs(x-p))
    return near
    
# =========================================================================== 
    
def fit_Grating_Eq(known_pix, known_wave, alpha, theta, Param):
    # Model # =============================================
    
    def Beta_Calc(w,a, FR, TF):
        beta = np.arcsin( (w*FR/1000000.0) - np.sin(a*np.pi/180.) )
        return beta
    def Predict_Pixel(X, FR, TF, ZPNT):
        a, w, t = X
        pPixel = np.tan((Beta_Calc(w,a, FR, TF) + (a*np.pi/180.)) - (TF*t*np.pi/180.)) * (fl/15.) + ZPNT
        return pPixel

    # Curve Fitting # =====================================
    Alpha= np.ones(np.shape(known_wave))*alpha  
    Theta= np.ones(np.shape(known_wave))*theta
    global fl 
    fr, fd, fl, zPnt= Param
    p0= [fr, fd, zPnt]
    xdata= [Alpha, known_wave, Theta] 
    Par, Covar = curve_fit(Predict_Pixel, xdata, known_pix, p0, maxfev= 10000)

    # Print Results # =====================================
    print '\nFitted Parameters:'
    print '\nLine Density= %s \nCam. Fudge= %s \nZero Pt. = %s'  % (Par[0], Par[1], Par[2])
    print '\nConstants: \nFocal Length = %s' % (fl)
    #print '\nCovarince Matrix: \n%s' % Covar

    # Variance of Parameters # ===============================
    # Calculated from Covariance matrix 
    Varience = []
    for i in range (0,len(Par)):
        P = np.zeros(len(Par))
        P[i] = 1
        Pt= np.transpose(P)
        C = np.asarray(Covar)
        SigSq = np.dot(P, np.dot(C,Pt) )
        Varience.append( np.sqrt(SigSq) )
    print "\nVariance of Parameters: \n%s" % Varience

    # Plot Residuals # =====================================
    X = zip(Alpha,known_wave,Theta)
    # Xb = zip(Alpha,known_wave)
    N = len(X)

    pPixel = [Predict_Pixel(X[n], Par[0],Par[1],Par[2]) for n in range(0,N)]
    Res = [known_pix[n]-pPixel[n] for n in range(0,N)]
    # print '\nResiduals:\n %s' % Res
    ChiSq = sum( [n**2. for n in Res] )
    #print '\nRaw ChiSq = %s' % ChiSq 
    print '\nReduced ChiSq = %s' % (ChiSq/(len(known_pix)-len(Par)-1))
    #print '\nMeanSqEr= %s\n' % (ChiSq/len(aPixel))
    plt.scatter(known_wave, Res, color='r', marker='+')
    plt.grid()
    plt.ylim( min(Res)*2., max(Res)*2.)
    plt.title('Least Squares Fit Residuals')
    plt.ylabel('Pixels')
    plt.xlabel('Wavelength')
    plt.show()

    savearray[0:len(known_wave),0] = known_wave
    savearray[0:len(Res),1] = Res
    
    return Par
    
# =========================================================================== 
def gaussmpfit(x,p): #single gaussian
    return p[3] +  p[0]*np.exp(-(((x-p[1])/(np.sqrt(2)*p[2])))**2.)


# =========================================================================== 
def fitgauss(p,fjac=None,x=None,y=None,err=None):
    #Parameter values are passed in p
    #fjac = None just means partial derivatives will not be computed
    model = gaussmpfit(x,p)
    status = 0
    return([status,(y-model)/err])

#===========================================    
def newzeropoint(x):
    beta = np.arctan( (bestpixel-x)*15./parm[2] ) + (n_fd*theta*np.pi/180.) - (alpha*np.pi/180.)
    out = newlambda - (10**6.)*( np.sin(beta) + np.sin(alpha*np.pi/180.) )/n_fr
    return out
    
# =========================================================================== 
    
def WaveShift(specname):
    #Calculates a new zero point for a spectrum based on a skyline
    spec_data= pf.getdata(specname)
    dataval = spec_data[2,0,:]
    spec_header= pf.getheader(specname)
    alpha= float( spec_header["GRT_TARG"] )
    theta= float( spec_header["CAM_TARG"] )
    
    trim_sec= spec_header["CCDSEC"]
    trim_offset= float( trim_sec[1:len(trim_sec)-1].split(':')[0] )-1
    bining= float( spec_header["PARAM18"] ) 
    nx= np.size(spec_data[0])
    Pixels= bining*(np.arange(0,nx,1)+trim_offset)
    WDwave = DispCalc(Pixels, alpha, theta, n_fr, n_fd, parm[2], n_zPnt)
    

    pix = range(len(dataval)) #This sets up an array of pixel numbers
    if 'red' in specname.lower():
        lowpix = 810 #For red setup. 6300 skyline
        highpix = 900 #For red setup. 6300 skyline
        skyline = 6300.304 #For red setup. 6300 skyline

    if 'blue' in specname.lower():
        #lowpix = 400 #For Ca K line
        #highpix = 465 #For Ca K line
        #skyline = 3933.668 #For Ca K line
        lowpix = 455  #For Ca H line
        highpix = 510 #For Ca H line
        skyline = 3968.4673 #For Ca H line
    
    fitdata = dataval[lowpix:highpix]
    fitpix = pix[lowpix:highpix]
    fiterror = np.sqrt(fitdata)

    if 'red' in specname.lower():
        guessgred = np.zeros(4)
        guessgred[3] = np.mean(fitdata) #continuum value
        guessgred[0] = np.max(fitdata) - guessgred[0] #amplitude
        guessgred[1] = fitpix[fitdata.argmax()] #central pixel
        guessgred[2] = 5. #guess at sigma
        paraminfo = [{'limits':[0,0],'limited':[0,0]} for i in range(4)]
        paraminfo[0]['limited'] = [1,0]
        paraminfo[0]['limits'] = [0.,0]
        fa = {'x':fitpix,'y':fitdata,'err':fiterror}
        fitsg = mpfit.mpfit(fitgauss,guessgred,functkw=fa,parinfo=paraminfo,quiet=True)
        #fitsg, fitsg_cov=curve_fit(Gauss,fitpix,fitdata,guessgred,maxfev=100000)
    
    if 'blue' in specname.lower():
        guessgblue = np.zeros(4)
        guessgblue[3] = np.mean(fitdata)
        guessgblue[0] = guessgblue[0] - np.min(fitdata)
        guessgblue[1] = fitpix[fitdata.argmin()] #minimum pixel
        guessgblue[2] = 5. #guess at sigma
        paraminfo = [{'limits':[0,0],'limited':[0,0]} for i in range(4)]
        paraminfo[0]['limited'] = [0,1]
        paraminfo[0]['limits'] = [0,0.]
        fa = {'x':fitpix,'y':fitdata,'err':fiterror}
        fitsg = mpfit.mpfit(fitgauss,guessgblue,functkw=fa,parinfo=paraminfo,quiet=True)
        #fitsg, fitsg_cov=curve_fit(Gauss,fitpix,fitdata,guessgblue,maxfev=100000)
    print 'Gaussian center at pixel ',fitsg.params[1]
    samp = np.arange(lowpix,highpix) # For plotting purposes
    fitfuncg = Gauss(samp,fitsg.params[0],fitsg.params[1],fitsg.params[2],fitsg.params[3])
    plt.hold('on')
    plt.plot(samp,fitfuncg,'r')
    plt.plot(fitpix,fitdata,'b')
    plt.axvline(x=fitsg.params[1],color='r')
    plt.hold('off')
    plt.show()

    savearray[0:len(samp),5] = samp
    savearray[0:len(samp),6] = fitdata
    savearray[0:len(samp),7] = fitfuncg

    #Take this fit and determine the new zero point
    global newlambda
    newlambda = skyline
    global bestpixel
    bestpixel = 2.*(fitsg.params[1] +trim_offset)#Need to figure out better way to take care of this 2
    guess = n_zPnt
    newzero = fsolve(newzeropoint,guess,xtol=1e-12)
    newzPnt = float(newzero)
    
    WDwave2 = DispCalc(Pixels, alpha, theta, n_fr, n_fd, parm[2], newzPnt)
    #plt.plot(WDwave2,spec_data[2,0,:])
    #plt.show()
    return newzPnt

# ===========================================================================
# Code ====================================================================== 
# ===========================================================================

#  Get Lamps # ==============================================================

from sys import argv
script, lamp = argv 

# Read Lamp Data and Header # 
lamp_data= pf.getdata(lamp)
lamp_header= pf.getheader(lamp)

# Check number of image slices, and select the spectra # 
if lamp_header["NAXIS"]== 2:
    lamp_spec= lamp_data[0]
elif lamp_header["NAXIS"]== 3:
    lamp_spec= lamp_data[0][0]
else:
    print ("\nDont know which data to unpack.")
    print ("Check the array dimensions\n")


# plt.figure(1)
# plt.plot(lamp_spec)
# plt.title('Raw')
# plt.show()

# Find the pixel number offset due to trim reindexing # 
trim_sec= lamp_header["CCDSEC"]
trim_offset= float( trim_sec[1:len(trim_sec)-1].split(':')[0] )-1

# Find Bining # 
bining= float( lamp_header["PARAM18"] ) 

# Get Pixel Numbers # 
nx= np.size(lamp_spec)
Pixels= bining*(np.arange(0,nx,1)+trim_offset)

# Select Set of Parameters to use # 
if lamp.__contains__('red'):
    parm= Param_930_20_40
    line_list= WaveList_Fe_930_20_40
elif lamp.__contains__('blue'):
    parm= Param_930_12_24
    line_list= WaveList_Fe_930_12_24
else: 
    print "Could not detect setup!" 

# Calculate Initial Guess Solution # ========================================

alpha= float( lamp_header["GRT_TARG"] )
theta= float( lamp_header["CAM_TARG"] )
Wavelengths= DispCalc(Pixels, alpha, theta, parm[0], parm[1], parm[2], parm[3])

# Plot Dispersion # 
plt.figure(1)
plt.plot(Wavelengths, lamp_spec)
plt.hold('on')
for line in line_list[1]:
    if (Wavelengths[0] <= line <= Wavelengths[-1]):
        plt.axvline(line, color= 'r', linestyle= '--')
plt.title("Initial Dispersion Inspection Graph. \nClose to Calculate Offset")
plt.xlabel("Wavelengths")
plt.ylabel("Counts")

plt.hold('off')
plt.show()

# Ask for offset # ===========================================================

print "\nWould You like to set Offset?" 
yn= raw_input('yes or no? >>> ')

#yn= 'yes'
if yn== 'yes':
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(Wavelengths, lamp_spec)
    plt.hold('on')
    for line in line_list[1]:
        if (Wavelengths[0] <= line <= Wavelengths[-1]):
            plt.axvline(line, color= 'r', linestyle= '--')
    plt.title("First click known line(red), then click coresponding peak near center\n Then close graph.")
    plt.xlabel("Wavelengths (Ang.)")
    plt.ylabel("Counts")
    if lamp.__contains__('blue'):
        plt.xlim(4700.,4900.)
    elif lamp.__contains__('red'):
        plt.xlim(6920.,7170.)
    plt.hold('off')
    coords= [] 
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    k_line= find_near(coords[0][0], line_list[1]) # Nearest line to click cordinates
    k_peak= find_near(coords[1][0], Wavelengths) # Nearest Peak to click cordinates
    i_peak= Wavelengths.index(k_peak)
    X= Wavelengths[i_peak-7:i_peak+7]
    Y= lamp_spec[i_peak-7:i_peak+7]
    amp, center, width, b= fit_Gauss(X,Y)
    offset= (k_line-center)
    Wavelengths= [w+offset for w in Wavelengths]

    plt.figure(1)
    plt.plot(Wavelengths, lamp_spec)
    plt.hold('on')
    for line in line_list[1]:
        if (Wavelengths[0] <= line <= Wavelengths[-1]):
            plt.axvline(line, color= 'r', linestyle= '--')
    plt.title("Offset Applied.")
    plt.xlabel("Wavelengths (Ang.)")
    plt.ylabel("Counts")
    plt.hold('off')
    plt.show()

# Ask Refit # ===============================================================
yn= 'yes'
while yn== 'yes':   
  
  print "\nWould you like to refit and recalculate dispersion?" 
  yn= raw_input('yes or no? >>> ')
  
  if yn== 'yes' :
        #print "\nOffset to apply to Grating Angle?"
        #alpha_offset= float( raw_input('Offset Value? >>>') )
        alpha_offset = 0.
        #alpha= alpha + alpha_offset
        '''
        #Uncomment this part if you would like to select lines to use by hand. Otherwise, all lines in the above line lists are used.
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        ax.plot(Wavelengths, lamp_spec)
        plt.hold('on')
        lines_in_range= []
        for line in line_list[1]:
            if (Wavelengths[0] <= line <= Wavelengths[-1]):
                lines_in_range.append(line)
                plt.axvline(line, color= 'r', linestyle= '--')
        plt.title("Click on The Peaks You Want to Use to Refit \n Then close graph.")
        plt.xlim([np.min(lines_in_range)-50, np.max(lines_in_range)+50])
        plt.ylim([np.min(lamp_spec)-100, np.max(lamp_spec)/2])
        plt.xlabel("Wavelengths (Ang.)")
        plt.ylabel("Counts")
        plt.hold('off')
        coords= [] 
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()    
        '''
        ###n_pnt, n_cor= np.shape(coords)
        ###coord_x= [coords[i][0] for i in range(0,n_pnt)]
        coord_x = line_list[1] #Use all lines in the line lists for the refitting.
        n_pnt = len(coord_x)
    
        peak_x= []
        for i in range(0,n_pnt):
            x= find_near(coord_x[i], Wavelengths)
            peak_x.append(x)
        centers_in_wave= find_peak_centers(peak_x, Wavelengths, lamp_spec)
        centers_in_wave= [w-offset for w in centers_in_wave]
        centers_in_pix= PixCalc(centers_in_wave, alpha, theta, parm[0], parm[1], parm[2], parm[3])
    
        known_waves= []
        for i in range(0,n_pnt):
            x= find_near(coord_x[i], line_list[1])
            known_waves.append(x)

        #Create array to save data for diagnostic purposes
        global savearray
        savearray = np.zeros([len(Wavelengths),8])
        n_fr, n_fd, n_zPnt= fit_Grating_Eq(centers_in_pix, known_waves, alpha, theta, parm)
        n_Wavelengths= DispCalc(Pixels, alpha-alpha_offset, theta, n_fr, n_fd, parm[2], n_zPnt)
        
        
        plt.figure(1)
        plt.plot(n_Wavelengths, lamp_spec)
        plt.hold('on')
        for line in line_list[1]:
            if (n_Wavelengths[0] <= line <= n_Wavelengths[-1]):
                plt.axvline(line, color= 'r', linestyle= '--')
        plt.title("Refitted Solution")
        plt.xlabel("Wavelengths (Ang.)")
        plt.ylabel("Counts")
        plt.hold('off')
        
        savearray[0:len(n_Wavelengths),2] = n_Wavelengths
        savearray[0:len(lamp_spec),3] = lamp_spec
        savearray[0:len(np.array(line_list[1])),4] = np.array(line_list[1])
        

        '''        
        plt.figure(2)
        Diff= [ (Wavelengths[i]-n_Wavelengths[i]) for i in range(0,np.size(Wavelengths)) ]
        plt.plot(Diff, '.')
        plt.title("Diffence between old and new solution.")
        plt.xlabel("Pixel")
        plt.ylabel("old-new Wavelength (Ang.)")
        '''

        plt.show()
        
# Save parameters in header and write file # 
print "\nWrite solution to header?"
yn= raw_input("yes or no? >>>")
if yn== "yes":    
    rt.Fix_Header(lamp_header)
    lamp_header.append( ('LINDEN', n_fr,'Line Desity for Grating Eq.'), 
                       useblanks= True, bottom= True )
    lamp_header.append( ('CAMFUD', n_fd,'Camera Angle Correction Factor for Grat. Eq.'), 
                       useblanks= True, bottom= True )
    lamp_header.append( ('FOCLEN', parm[2],'Focal Length for Grat Eq.'), 
                       useblanks= True, bottom= True )
    lamp_header.append( ('ZPOINT', n_zPnt,'Zero Point Pixel for Grat Eq.'), 
                       useblanks= True, bottom= True )        
    NewHdu = pf.PrimaryHDU(data= lamp_data, header= lamp_header)
    NewHdu.writeto('w'+lamp, output_verify='warn', clobber= True)

#Save parameters to ZZ Ceti spectrum#
print "\nWrite solution to header of another spectrum?"
yn= raw_input("yes or no? >>>")
if yn== "yes":
    specname = raw_input("Filename: ")
    newzeropoint = WaveShift(specname)
    spec_data= pf.getdata(specname)
    spec_header= pf.getheader(specname)
    rt.Fix_Header(spec_header)
    spec_header.append( ('LINDEN', n_fr,'Line Desity for Grating Eq.'), 
                       useblanks= True, bottom= True )
    spec_header.append( ('CAMFUD', n_fd,'Camera Angle Correction Factor for Grat. Eq.'), 
                       useblanks= True, bottom= True )
    spec_header.append( ('FOCLEN', parm[2],'Focal Length for Grat Eq.'), 
                       useblanks= True, bottom= True )
    spec_header.append( ('ZPOINT', newzeropoint,'Zero Point Pixel for Grat Eq.'), 
                       useblanks= True, bottom= True )        
    NewspecHdu = pf.PrimaryHDU(data= spec_data, header= spec_header)
    NewspecHdu.writeto('w'+specname, output_verify='warn', clobber= True)

#Save arrays for diagnostics
now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
endpoint = '_930'
with open('wavecal_' + specname[4:specname.find(endpoint)] + '_' + now + '.txt','a') as handle:
    header = lamp + ',' + specname + '\n First 2 columns: fitted wavelengths, residuals \n Next 3 columns: wavelengths, flux, lambdas fit \n Final 3 columns: wavelengths, sky flux, fit to line for recentering'
    np.savetxt(handle,savearray,fmt='%f',header = header)
    
    
# ==========================================================================
    
    '''
        # This is the falied cross corelation reffiting code # 
    
        Corr= CrossCorr(lamp_spec) # Cross correlate with gaussian 
        peak_x, peak_y = PeakFind(Corr) # find peaks of cross correlation 
        centers= find_peak_centers(peak_x, Corr) # Find Centers of identified peaks 
        centers= [2.0*(c+trim_offset) for c in centers] # Account for trim and bining
    
        plt.figure(1)
        plt.plot(Pixels,Corr)
        plt.hold('on')
        plt.scatter(centers, peak_y, marker= '*')
        plt.scatter([2.0*(x+trim_offset) for x in peak_x] , peak_y, marker= '+')
        plt.hold('off')
        plt.title("Identified Peak Centers" )
        plt.show()
    
        # predict wavelength of centers using know parameters # 
        predict_wave= DispCalc(centers, alpha, theta, parm[0], parm[1], parm[2], parm[3] )
    
        # find wavelength in list that is closest to predicted wave # 
        known_pix= []
        known_waves= []
        id_centers= [] 
        for i in range(0,np.size(predict_wave)):
            pw= predict_wave[i]
            kw= find_near(pw, line_list[1]) # Nearest Known Wave
            if np.abs(kw-pw) <= 20.0:
                idx= (np.abs(line_list[1] - kw)).argmin() # index of kw with the list
                kp= line_list[0][idx]
                id_centers.append( centers[i]) # known Id'd centers to use for fit # 
                known_waves.append( kw )
                known_pix.append( kp )
        print ("%4.4f, %4.4f, %4.4f") % (centers[i], pw , kw)
    
        n_fr, n_fd, n_zPnt= fit_Grating_Eq(id_centers, known_waves, alpha, theta, parm)
    
        n_Wavelengths= DispCalc(Pixels, alpha, theta, n_fr, n_fd, parm[3], n_zPnt)
    
        plt.figure(1)
        plt.plot(n_Wavelengths, lamp_spec)
        plt.hold('on')
        for line in line_list[1]:
            if (n_Wavelengths[0] <= line <= n_Wavelengths[-1]):
                plt.axvline(line, color= 'r', linestyle= '--')
        plt.title("Refitted Dispersion")
        plt.xlabel("Wavelengths")
        plt.ylabel("Counts")
        plt.hold('off')
        plt.show()
        
    '''
