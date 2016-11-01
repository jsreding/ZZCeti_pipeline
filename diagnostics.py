# -*- coding: utf-8 -*-
"""
Diagnostic Plots for Pipeline
Author: Patrick O'Brien
Date: October 2016
"""
# Import statements
from glob import glob
import os
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileMerger

# function that takes file names and organizes by the unique star name in each
def unique_star_names(seq, idfun=None): 
       # order preserving
       if idfun is None:
           def idfun(x): return x
       seen = {}
       result = []
       for item in seq:
           marker = idfun(item)
           if marker in seen: continue
           seen[marker] = 1
           result.append(item)
       return result
       
##### ------------------------------------------------------------------ #####
# Calibrations function
def diagnostic_plots_cals(file_name):
    pp = PdfPages('cal_plots.pdf')

    arr = np.genfromtxt(file_name, dtype=None, delimiter=' ')
    
    bias_bs, bias_as, bias_std = [],[],[]
    flat_blue_bs, flat_blue_std_bs, flat_blue_as, flat_blue_std_as = [],[],[], []
    flat_red_bs, flat_red_std_bs, flat_red_as, flat_red_std_as = [],[],[], []
    blue_pix, blue_val, blue_poly = [],[],[]
    red_pix, red_val, red_poly = [],[],[]

    for m in np.arange(len(arr)):
    
        bias_bs.append(arr[m][0])
        bias_as.append(arr[m][1])
        bias_std.append(arr[m][2])
        
        flat_blue_bs.append(arr[m][3])
        flat_blue_std_bs.append(arr[m][4])
        flat_blue_as.append(arr[m][5])
        flat_blue_std_as.append(arr[m][6])
    
        flat_red_bs.append(arr[m][7])
        flat_red_std_bs.append(arr[m][8])
        flat_red_as.append(arr[m][9])
        flat_red_std_as.append(arr[m][10])
        
        blue_pix.append(arr[m][11])
        blue_val.append(arr[m][12])
        blue_poly.append(arr[m][13])
        
        red_pix.append(arr[m][14])
        red_val.append(arr[m][15])
        red_poly.append(arr[m][16])
    
    bias_bs = np.array(bias_bs)
    bias_bs = bias_bs[bias_bs != 0.0]
    bias_bs = np.array(bias_bs)
    
    bias_as = np.array(bias_as)
    bias_as = bias_as[bias_as != 0.0]
    bias_as = np.array(bias_as)
    
    bias_std = np.array(bias_std)
    bias_std = bias_std[bias_std != 0.0]
    bias_std = np.array(bias_std)
    
    flat_blue_bs = np.array(flat_blue_bs)
    flat_blue_bs = flat_blue_bs[flat_blue_bs != 0.0]
    flat_blue_bs = np.array(flat_blue_bs)
    
    flat_blue_as = np.array(flat_blue_as)
    flat_blue_as = flat_blue_as[flat_blue_as != 0.0]
    flat_blue_as = np.array(flat_blue_as)
    
    flat_blue_std_bs = np.array(flat_blue_std_bs)
    flat_blue_std_bs = flat_blue_std_bs[flat_blue_std_bs != 0.0]
    flat_blue_std_bs = np.array(flat_blue_std_bs)
    
    flat_blue_std_as = np.array(flat_blue_std_as)
    flat_blue_std_as = flat_blue_std_as[flat_blue_std_as != 0.0]
    flat_blue_std_as = np.array(flat_blue_std_as)
    
    flat_red_bs = np.array(flat_red_bs)
    flat_red_bs = flat_red_bs[flat_red_bs != 0.0]
    flat_red_bs = np.array(flat_red_bs)
    
    flat_red_as = np.array(flat_red_as)
    flat_red_as = flat_red_as[flat_red_as != 0.0]
    flat_red_as = np.array(flat_red_as)
    
    flat_red_std_bs = np.array(flat_red_std_bs)
    flat_red_std_bs = flat_red_std_bs[flat_red_std_bs != 0.0]
    flat_red_std_bs = np.array(flat_red_std_bs)
    
    flat_red_std_as = np.array(flat_red_std_as)
    flat_red_std_as = flat_red_std_as[flat_red_std_as != 0.0]
    flat_red_std_as = np.array(flat_red_std_as)
    
    blue_pix = np.array(blue_pix)
    blue_pix = blue_pix[blue_pix != 0.0]
    blue_pix = np.array(blue_pix)
    
    blue_val = np.array(blue_val)
    blue_val = blue_val[blue_val != 0.0]
    blue_val = np.array(blue_val)
    
    blue_poly = np.array(blue_poly)
    blue_poly = blue_poly[blue_poly != 0.0]
    blue_poly = np.array(blue_poly)
    
    red_pix = np.array(red_pix)
    red_pix = red_pix[red_pix != 0.0]
    red_pix = np.array(red_pix)
    
    red_val = np.array(red_val)
    red_val = red_val[red_val != 0.0]
    red_val = np.array(red_val)
    
    red_poly = np.array(red_poly)
    red_poly = red_poly[red_poly != 0.0]
    red_poly = np.array(red_poly)

    plt.figure()
    plt.errorbar(np.arange(len(bias_bs)), bias_bs, yerr=bias_std, marker="o", linestyle="None")
    plt.xlabel('Number')
    plt.ylabel('Value')
    plt.title('Bias - Before Scaling')
    plt.savefig(pp,format='pdf')
    
    plt.figure()
    plt.errorbar(np.arange(len(bias_as)), bias_as, yerr=bias_std, marker="o", linestyle="None")
    plt.xlabel('Number')
    plt.ylabel('Value')
    plt.title('Bias - After Scaling')
    plt.savefig(pp,format='pdf')
    
    plt.figure()
    plt.errorbar(np.arange(len(flat_blue_bs)), flat_blue_bs, yerr=flat_blue_std_bs, marker="o", linestyle="None")
    plt.xlabel('Number')
    plt.ylabel('Value')
    plt.title('Blue Flat - Before Scaling')
    plt.savefig(pp,format='pdf')
    
    plt.figure()
    plt.errorbar(np.arange(len(flat_blue_as)), flat_blue_as, yerr=flat_blue_std_as, marker="o", linestyle="None")
    plt.xlabel('Number')
    plt.ylabel('Value')
    plt.title('Blue Flat - After Scaling')
    plt.savefig(pp,format='pdf')
    
    if len(flat_red_bs) > 0:
        plt.figure()
        plt.errorbar(np.arange(len(flat_red_bs)), flat_red_bs, yerr=flat_red_std_bs, ecolor='r', marker="o",markerfacecolor='r', linestyle="None")
        plt.xlabel('Number')
        plt.ylabel('Value')
        plt.title('Red Flat - Before Scaling')
        plt.savefig(pp,format='pdf')
    
        plt.figure()
        plt.errorbar(np.arange(len(flat_red_as)), flat_red_as, yerr=flat_red_std_as, ecolor='r', marker="o",markerfacecolor='r', linestyle="None")
        plt.xlabel('Number')
        plt.ylabel('Value')
        plt.title('Red Flat - After Scaling')
        plt.savefig(pp,format='pdf')
    
    plt.figure()
    plt.plot(blue_pix, blue_val,'o')
    plt.plot(np.arange(len(blue_poly)),blue_poly,'g')
    plt.xlabel('Pixel')
    plt.ylabel('Value')
    plt.title('Blue Polynomial Check')
    plt.savefig(pp,format='pdf')
    
    if len(red_val > 0):
        plt.figure()
        plt.plot(red_pix, red_val,'ro')
        plt.plot(np.arange(len(red_poly)),red_poly,'g')
        plt.xlabel('Pixel')
        plt.ylabel('Value')
        plt.title('Red Polynomial Check')
        plt.savefig(pp,format='pdf')
    
    pp.close()
    
##### ------------------------------------------------------------------ #####
# FWHM function
def diagnostic_plots_FWHM(file_name):
    pp = PdfPages('fwhm_plots.pdf')
    
    def unique_star_names(seq, idfun=None): 
       # order preserving
       if idfun is None:
           def idfun(x): return x
       seen = {}
       result = []
       for item in seq:
           marker = idfun(item)
           # in old Python versions:
           # if seen.has_key(marker)
           # but in new ones:
           if marker in seen: continue
           seen[marker] = 1
           result.append(item)
       return result
    
    arr = np.genfromtxt(file_name, dtype=None,delimiter='\t')
    
    names, col1, fwhm1, pos1, col2, fwhm2, pos2 = [],[],[],[],[],[],[]
    for m in np.arange(len(arr)):
        #print m
        names.append(str(arr[m][0][8:]))
        col1.append(arr[m][1])
        fwhm1.append(arr[m][2])    
        pos1.append(arr[m][3])
        col2.append(arr[m][4])
        fwhm2.append(arr[m][5])   
        pos2.append(arr[m][6])
    fwhm1 = np.array(fwhm1)
    col1 = np.array(col1)
    pos1 = np.array(pos1)
    #unique_names = set(names)
    #print unique_names
    
    only_star_names = []
    for i in names:
        only_star_names.append(i.split("_")[0])
    
    unique_names = unique_star_names(only_star_names)

    cat_pts = []
    fwhm_pts = []
    for i in range(len(names)):
        for j in range(len(unique_names)):
            if unique_names[j] in names[i]:
                cat_pts.append(j)
                fwhm_pts.append(fwhm1[i])
    
    x = np.arange(len(unique_names))
    jitter = 0.1*np.random.rand(len(cat_pts))
    cat_pts = cat_pts + jitter
    
    plt.figure()
    plt.xticks(x, unique_names)
    plt.scatter(cat_pts,fwhm1)
    plt.xlabel('Star')
    plt.ylabel('Value')
    plt.title('FWHM')
    plt.savefig(pp,format='pdf')
    
    plt.figure()
    plt.xticks(x, unique_names)
    plt.scatter(cat_pts, pos1)
    plt.xlabel('Star')
    plt.ylabel('Value')
    plt.title('Profile Position')
    plt.savefig(pp,format='pdf')
    
    pp.close()
   
##### ------------------------------------------------------------------ #####
# Wavelength calibrations function
def diagnostic_plots_wavecal(files):
    
    star_name = str(files[0][8:-21])
    pdf_name = 'wavecal_plots_' + star_name + '.pdf'
    pp = PdfPages(pdf_name)
    
    with open(files[0], 'r') as f:
        first_line = f.readline()
        if 'blue' in first_line:
            blue_arr = np.genfromtxt(files[0],dtype=None,delimiter=' ')
        elif 'red' in first_line:
            red_arr = np.genfromtxt(files[0],dtype=None,delimiter=' ')
    red_arr = []
    if len(files) > 1:
        with open(files[1],'r') as f:
            first_line = f.readline()
            if 'blue' in first_line:
                blue_arr = np.genfromtxt(files[1],dtype=None,delimiter=' ')
            elif 'red' in first_line:
                red_arr = np.genfromtxt(files[1],dtype=None,delimiter=' ')

    wave_fit, res, wave1, flux1, lam_fit, wave2, flux2, line_fit = [],[],[],[],[],[],[],[]
    
    for m in np.arange(len(blue_arr)):
    
        wave_fit.append(blue_arr[m][0])
        res.append(blue_arr[m][1])
        
        wave1.append(blue_arr[m][2])
        flux1.append(blue_arr[m][3])
        lam_fit.append(blue_arr[m][4])
        
        wave2.append(blue_arr[m][5])
        flux2.append(blue_arr[m][6])
        line_fit.append(blue_arr[m][7])
    
    wave_fit = np.array(wave_fit)
    wave_fit = wave_fit[wave_fit != 0.0]
    wave_fit = np.array(wave_fit)
    
    res = np.array(res)
    res = res[res != 0.0]
    res = np.array(res)
    
    wave1 = np.array(wave1)
    wave1 = wave1[wave1 != 0.0]
    wave1 = np.array(wave1)
    
    lam_fit = np.array(lam_fit)
    lam_fit = lam_fit[lam_fit != 0.0]
    lam_fit = np.array(lam_fit)
    
    flux1 = np.array(flux1)
    flux1 = flux1[flux1 != 0.0]
    flux1 = np.array(flux1)
    
    wave2 = np.array(wave2)
    wave2 = wave2[wave2 != 0.0]
    wave2 = np.array(wave2)
    
    flux2 = np.array(flux2)
    flux2 = flux2[flux2 != 0.0]
    flux2 = np.array(flux2)
    
    line_fit = np.array(line_fit)
    line_fit = line_fit[line_fit != 0.0]
    line_fit = np.array(line_fit)
    
    xmin = np.min(wave_fit)-500
    xmax = np.max(wave_fit)+500
    x = np.linspace(xmin,xmax,1000)
    zeros = np.zeros(len(x))
    plt.figure()
    plt.scatter(wave_fit,res)
    plt.plot(x,zeros,'b--')
    plt.xlim(xmin,xmax)
    plt.xlabel('Wavelength')
    plt.ylabel('Residual')
    plt.title('Wavelength Fit Residuals - Blue - ' + star_name)
    plt.savefig(pp,format='pdf')

    plt.figure()
    plt.plot(wave1,flux1)
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title('Flux - Blue - ' + star_name)
    plt.savefig(pp,format='pdf')

    x_line = np.linspace(np.min(wave2),np.max(wave2),len(line_fit))
    plt.figure()
    plt.plot(wave2,flux2)
    plt.plot(x_line,line_fit)
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title('Sky Flux - Blue - ' + star_name)
    plt.savefig(pp,format='pdf')
    
    ### ---------------------------------------------------------------------- ###
    if len(red_arr) > 0:
        wave_fit, res, wave1, flux1, lam_fit, wave2, flux2, line_fit = [],[],[],[],[],[],[],[]
        
        for m in np.arange(len(red_arr)):
        
            wave_fit.append(red_arr[m][0])
            res.append(red_arr[m][1])
            
            wave1.append(red_arr[m][2])
            flux1.append(red_arr[m][3])
            lam_fit.append(red_arr[m][4])
            
            wave2.append(red_arr[m][5])
            flux2.append(red_arr[m][6])
            line_fit.append(red_arr[m][7])
        
        wave_fit = np.array(wave_fit)
        wave_fit = wave_fit[wave_fit != 0.0]
        wave_fit = np.array(wave_fit)
        
        res = np.array(res)
        res = res[res != 0.0]
        res = np.array(res)
        
        wave1 = np.array(wave1)
        wave1 = wave1[wave1 != 0.0]
        wave1 = np.array(wave1)
        
        lam_fit = np.array(lam_fit)
        lam_fit = lam_fit[lam_fit != 0.0]
        lam_fit = np.array(lam_fit)
        
        flux1 = np.array(flux1)
        flux1 = flux1[flux1 != 0.0]
        flux1 = np.array(flux1)
        
        wave2 = np.array(wave2)
        wave2 = wave2[wave2 != 0.0]
        wave2 = np.array(wave2)
        
        flux2 = np.array(flux2)
        flux2 = flux2[flux2 != 0.0]
        flux2 = np.array(flux2)
        
        line_fit = np.array(line_fit)
        line_fit = line_fit[line_fit != 0.0]
        line_fit = np.array(line_fit)
        
        xmin = np.min(wave_fit)-500
        xmax = np.max(wave_fit)+500
        x = np.linspace(xmin,xmax,1000)
        zeros = np.zeros(len(x))
        plt.figure()
        plt.scatter(wave_fit,res,color='red')
        plt.plot(x,zeros,'r--')
        plt.xlim(xmin,xmax)
        plt.xlabel('Wavelength')
        plt.ylabel('Residual')
        plt.title('Wavelength Fit Residuals - Red - ' + star_name)
        plt.savefig(pp,format='pdf')
        
        plt.figure()
        plt.plot(wave1,flux1,'r')
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.title('Flux - Red - ' + star_name)
        plt.savefig(pp,format='pdf')
       
        x_line = np.linspace(np.min(wave2),np.max(wave2),len(line_fit))
        plt.figure()
        plt.plot(wave2,flux2,'r')
        plt.plot(x_line,line_fit,'g')
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.title('Sky Flux - Red - ' + star_name)
        plt.savefig(pp,format='pdf')
    
    pp.close()

##### ------------------------------------------------------------------ #####
# Continuum function
def diagnostic_plots_continuum(file_name):
    
    star_name = str(file_name[24:-21])
    pdf_name = 'modelcal_plots_' + star_name + '.pdf'
    pp = PdfPages(pdf_name)

    arr = np.genfromtxt(file_name, dtype=None, delimiter=' ')

    blue_lam, blue_res, blue_masked_lam, blue_masked_res, blue_res_fit, norm_spec_blue = [],[],[],[],[],[]

    for m in np.arange(len(arr)):
    
        blue_lam.append(arr[m][0])
        blue_res.append(arr[m][1])
        
        blue_masked_lam.append(arr[m][2])
        blue_masked_res.append(arr[m][3])
        blue_res_fit.append(arr[m][4])
        
        norm_spec_blue.append(arr[m][5])

    blue_lam = np.array(blue_lam)
    blue_lam = blue_lam[blue_lam != 0.0]
    blue_lam = np.array(blue_lam)
    
    blue_res = np.array(blue_res)
    blue_res = blue_res[blue_res != 0.0]
    blue_res = np.array(blue_res)
    
    blue_masked_lam = np.array(blue_masked_lam)
    blue_masked_lam = blue_masked_lam[blue_masked_lam != 0.0]
    blue_masked_lam = np.array(blue_masked_lam)
    
    blue_masked_res = np.array(blue_masked_res)
    blue_masked_res = blue_masked_res[blue_masked_res != 0.0]
    blue_masked_res = np.array(blue_masked_res)
    
    blue_res_fit = np.array(blue_res_fit)
    blue_res_fit = blue_res_fit[blue_res_fit != 0.0]
    blue_res_fit = np.array(blue_res_fit)
    
    norm_spec_blue = np.array(norm_spec_blue)
    norm_spec_blue = norm_spec_blue[norm_spec_blue != 0.0]
    norm_spec_blue = np.array(norm_spec_blue)

    plt.figure()
    plt.plot(blue_lam, blue_res)
    plt.plot(blue_masked_lam, blue_masked_res)
    plt.plot(blue_lam, blue_res_fit)
    
    plt.xlabel('Wavelength')
    plt.ylabel('Response')
    plt.title('Response - Blue - ' + star_name)
    plt.savefig(pp,format='pdf')
    
    plt.figure()
    plt.plot(blue_lam, norm_spec_blue)
    plt.xlabel('Wavelength')
    plt.ylabel('Spectrum')
    plt.title('Continuum Normalized Spectrum - Blue')
    plt.savefig(pp,format='pdf')
     
    ### ---------------------------------------------------------------------- ###
    if len(arr[0]) > 6:    
        red_lam, red_res, red_masked_lam, red_masked_res, red_res_fit, norm_spec_red = [],[],[],[],[],[]

        for m in np.arange(len(arr)):
        
            red_lam.append(arr[m][6])
            red_res.append(arr[m][7])
            
            red_masked_lam.append(arr[m][8])
            red_masked_res.append(arr[m][9])
            red_res_fit.append(arr[m][10])
            
            norm_spec_red.append(arr[m][11])
    
        red_lam = np.array(red_lam)
        red_lam = red_lam[red_lam != 0.0]
        red_lam = np.array(red_lam)
        
        red_res = np.array(red_res)
        red_res = red_res[red_res != 0.0]
        red_res = np.array(red_res)
        
        red_masked_lam = np.array(red_masked_lam)
        red_masked_lam = red_masked_lam[red_masked_lam != 0.0]
        red_masked_lam = np.array(red_masked_lam)
        
        red_masked_res = np.array(red_masked_res)
        red_masked_res = red_masked_res[red_masked_res != 0.0]
        red_masked_res = np.array(red_masked_res)
        
        red_res_fit = np.array(red_res_fit)
        red_res_fit = red_res_fit[red_res_fit != 0.0]
        red_res_fit = np.array(red_res_fit)
        
        norm_spec_red = np.array(norm_spec_red)

        plt.figure()
        plt.plot(red_lam, red_res)
        plt.plot(red_masked_lam, red_masked_res)
        plt.plot(red_lam, red_res_fit)
        plt.xlabel('Wavelength')
        plt.ylabel('Response')
        plt.title('Response - Red - ' + star_name)
        plt.savefig(pp,format='pdf')
        
        plt.figure()
        plt.plot(red_lam, norm_spec_red,'r')
        plt.xlabel('Wavelength')
        plt.ylabel('Spectrum')
        plt.title('Continuum Normalized Spectrum - Red')
        plt.savefig(pp,format='pdf')
    
    pp.close()
  
##### ------------------------------------------------------------------ #####
# Extraction function
def diagnostic_plots_extraction(file_name):
    pp = PdfPages('extraction_plots.pdf')

    arr = np.genfromtxt(file_name, dtype=None, delimiter=' ')

    meas_FWHM, pix_FWHM, fit_FWHM, all_pix = [],[],[],[]
    prof_pix, prof_pos, fit_prof_pos = [],[],[]
    
    for m in np.arange(len(arr)):
        meas_FWHM.append(arr[m][0])
        pix_FWHM.append(arr[m][1])
        fit_FWHM.append(arr[m][2])
        all_pix.append(arr[m][3])
        
        prof_pix.append(arr[m][4])
        prof_pos.append(arr[m][5])
        fit_prof_pos.append(arr[m][6])
        
    meas_FWHM = np.array(meas_FWHM)
    meas_FWHM = meas_FWHM[meas_FWHM != 0.0]
    meas_FWHM = np.array(meas_FWHM)

    pix_FWHM = np.array(pix_FWHM)
    pix_FWHM = pix_FWHM[pix_FWHM != 0.0]
    pix_FWHM = np.array(pix_FWHM)

    fit_FWHM = np.array(fit_FWHM)
    fit_FWHM = fit_FWHM[fit_FWHM != 0.0]
    fit_FWHM = np.array(fit_FWHM)
    
    all_pix = np.array(all_pix)
    all_pix = all_pix[all_pix != 0.0]
    all_pix = np.array(all_pix)
    
    prof_pix = np.array(prof_pix)
    prof_pix = prof_pix[prof_pix != 0.0]
    prof_pix = np.array(prof_pix)
    
    prof_pos = np.array(prof_pos)
    prof_pos = prof_pos[prof_pos != 0.0]
    prof_pos = np.array(prof_pos)
    
    fit_prof_pos = np.array(fit_prof_pos)
    fit_prof_pos = fit_prof_pos[fit_prof_pos != 0.0]
    fit_prof_pos = np.array(fit_prof_pos)
    
    plt.figure()
    plt.scatter(pix_FWHM,meas_FWHM)
    plt.plot(np.arange(len(fit_FWHM)),fit_FWHM)
    plt.xlabel('Pixel')
    plt.ylabel('FWHM')
    plt.title('Extraction FWHM')
    plt.savefig(pp,format='pdf')
    
    plt.figure()
    plt.scatter(prof_pix,prof_pos)
    plt.plot(np.arange(len(fit_prof_pos)),fit_prof_pos)
    plt.xlabel('Pixel')
    plt.ylabel('Profile Position')
    plt.title('Extraction Profile')
    plt.savefig(pp,format='pdf')
    
    pp.close()

##### ------------------------------------------------------------------ #####    
# Sort file names by type
cal_files = glob('reduction*.txt')
fwhm_files = glob('FWHM*.txt')
wave_cal_files = glob('wavecal*.txt')
model_cal_files = glob('continuum_normalization*.txt')
extraction_files = glob('extraction_*_*.txt')

##### ------------------------------------------------------------------ #####
# Calibrations
for i in range(len(cal_files)): # Repeat copy of data below
    file_name = str(cal_files[i])
    diagnostic_plots_cals(file_name)

##### ------------------------------------------------------------------ #####
# FWHM
for i in range(len(fwhm_files)):    # First line not commented out
    file_name = str(fwhm_files[i])
    diagnostic_plots_FWHM(file_name)

##### ------------------------------------------------------------------ #####
# Wavelength Calibrations
star_names = []
for i in range(len(wave_cal_files)):
    star_names.append(wave_cal_files[i][8:-21])
    with open(wave_cal_files[i], 'r') as f:
        first_line = f.readline()
        #print first_line

unique_names = unique_star_names(star_names)

for sub in unique_names:
    file_names = [x for x in wave_cal_files if str(sub) in x]
    diagnostic_plots_wavecal(file_names)
 
##### ------------------------------------------------------------------ #####
# Model Calibrations

star_names = []
for i in range(len(model_cal_files)):
    star_names.append(model_cal_files[i][24:-21])
    with open(model_cal_files[i], 'r') as f:
        first_line = f.readline()

unique_names = unique_star_names(star_names)

for sub in unique_names:
    file_name = [x for x in model_cal_files if str(sub) in x]
    diagnostic_plots_continuum(file_name[0])

##### ------------------------------------------------------------------ #####
# Extraction
for i in range(len(extraction_files)): # Repeat copy of data below
    file_name = str(extraction_files[i])
    diagnostic_plots_extraction(file_name)
     
######------------------------------------------------------------------ #####
# Merge all pdfs of plots
pdfs = glob('*.pdf')
outfile = PdfFileMerger()

for f in pdfs:
    outfile.append(open(f, 'rb'))
    os.remove(f)
    
outfile.write(open('diagnostic_plots.pdf', 'wb'))

