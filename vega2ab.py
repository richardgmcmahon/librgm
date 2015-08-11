from __future__ import division, print_function


"""
TODO: implement reverse operation: i.e. AB -> Vega

Also need to add explicit add VISTA, VHS, DES

"""

"""

 based on libvista/wise_vega2ab


;
; Convert published WISE magnitudes which are in the Vega system to
; a range of alternaive flux estimators:
;  (i)   AB magnitudes 
;  (ii)  Fnu in Jansky Jy
;  (iii) Fnu in SI units: W Hz-1 m-2
;  (iv)  Fnu in cgs units erg Hz^-1 cm^-2
;  (v)   nuFnu in SI units W m-2
;  (vi)  nuFnu  in cgs unit erg s-1 cm-2
; 
; The AB system is defined such that every filter has a zero-point
; flux density of 3631 Jy 
; (1 Jy = 1 Jansky = 10-26 W Hz-1 m-2 = 10-23 erg s-1 Hz-1 cm-2).
;
; A object with AB=0 has a flux of 3631Jy
;
; 2.5*log10(3631) = 8.90
; 2.5*log10(3631*10^-23) = 48.60
;
; SDSS photometry is intended to be on the AB system 
; Oke, J.B., & Gunn, J.E. 1983, ApJ, 266, 713 
;   
; see also
; Oke, J.B. 1974, ApJS, 27, 21 
;   'Absolute Spectral Energy Distributions for White Dwarfs'
;
; Absolute magnitude of 0 (ie 10pc Mag) 4.345 x 10^13 W Hz^-1
;
; see also http://www.astro.ljmu.ac.uk/~ikb/convert-units/node4.html
;
; WISE photometry is on the Vega system and defined in
; Wright et al , 2010AJ....140.1868W.
; http://adsabs.harvard.edu/abs/2010AJ....140.1868W
; see alos
; http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4h.html#Summary
;
; http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4h.html#conv2flux

; From Wright et al the Vega zeropoints in W[1-4] are:
; 306.681 Jy
; 170.663
; 29.0448 
; 8.2839 
;
; The IPAC tables have values of:
; 306.682 for the W1 zero point 
;
;
; The nominal central wavelengths are 
; 3.3526, 4.6028, 11.5608, and 22.0883 um for W1,..., W4
;
; 8.180 x 10-15
; 2.415 x 10-15
; 6.515 x 10-17
; 5.090 x 10-18 W cm-2 um-1 
;

"""



import os, sys
import math
import string
import traceback

import numpy as np

def convert(mag, waveband, wavebands, AB_offset, nu_filter,
  AB=False, test=False, jy=False, nuFnu=False, 
  cgs=False, siflux=False, debug=False, verbose=False):


  for (iband, waveband_test) in enumerate(wavebands):

      if waveband.upper() == waveband_test.upper():

        if debug: print('waveband_test: ', waveband_test)
        if debug: print('waveband: ', waveband.upper())
        if debug or verbose: 
          print('Computing for waveband: ', waveband, waveband_test)

        # default is to convert to AB
        if not jy: 
          if not AB:
            result= mag + AB_offset[iband]
          if AB:
            result= mag 
          if verbose: print('Result: ', mag, ' >> ', result)

        if jy or nuFnu:
          # compute the AB magnitude
          if AB: abmag = mag
          if not AB: abmag = (mag+AB_offset[iband])

          # compute the SI flux in  W Hz-1 m-2
          siflux=10**(-0.4*abmag)*(3631.0*1e-26)

        if jy: result=10**(-0.4*abmag)*(3631.0) # Jy
        if siflux: result = siflux
        if nuFnu: result  = siflux * nu_filter[iband]

        if cgs:
          result=-99.9 
          print('cgs not implemented yet')

  return result



def sdss(mag=0.0, waveband='i', AB=False,
  test=False, jy=False, nuFnu=False, 
  cgs=False, siflux=False, debug=False, verbose=False):

  """
    Convert Vega to AB ma gnitudes using the Hewett etal(2006) conversion
    2006MNRAS.367..454H,
  
  """

  system='sdss'

  wavebands=['u','g','r','i','z']

  # from Hewett et al. 2009
  AB_offset=[0.927, 0.103, 0.146, 0.366, 0.533]

#The nominal central wavelengths in microns
  filter_wavelength=np.array([0.3546, 0.4670, 0.6156, 0.7471, 0.8918]) # microns

# Speed of light
  c = 299792458.0 # m s^-1

# Frequency for each filter; 1e-6 converts the filter 
# central wavelengths to m s^-1
  nu_filter=c/(filter_wavelength*1e-6)

  if test:
    result=testit(wavebands, nu_filter, system=system)
    
# do the conversion
  if not test:
    result=convert(mag, waveband, wavebands, AB_offset, nu_filter, AB=AB)

  return result


def wfcam(mag=0.0, waveband='Y', AB=False,
  test=False, jy=False, nuFnu=False, 
  cgs=False, siflux=False, debug=False, verbose=False):

  """
  ;  Convert Vega to AB ma gnitudes using the Hewett etal(2006) conversion
  ;  2006MNRAS.367..454H,
  ;  Oke, J.B. 1974, ApJS, 27, 21
  """

  system='wfcam'

  wavebands=['Z','Y','J','H','K']

  AB_offset=[0.528,0.634, 0.938, 1.379, 1.900]

#The nominal central wavelengths in microns
  filter_wavelength=np.array([0.8817, 1.0305, 1.2483, 1.6313, 2.2010]) # microns

# Speed of light
  c = 299792458.0 # m s^-1

# Frequency for each filter; 1e-6 converts the filter 
# central wavelengths to m s^-1
  nu_filter=c/(filter_wavelength*1e-6)

  if test:
   result=testit(wavebands, nu_filter, system=system, AB=AB)
  
# do the conversion
  if not test:
    result=convert(mag, waveband, wavebands, AB_offset, nu_filter, AB=AB)

  return result


def wise(mag=0.0, waveband='W1', AB_Tokunaga_2005=False,
  AB=False, test=False, jy=False, nuFnu=False, 
  cgs=False, siflux=False, debug=False, verbose=False):

  """

  based on the rgm's IDL procedure libvista/wise_vega2ab.pro


  """

  system='wise'

  if verbose or test: print('vegamag: ', mag)
  if verbose or test: print('waveband:',waveband) 


#  WISE waveband names
  wavebands=['W1','W2','W3','W4']

  # Wright et al, 2010
  # http://adsabs.harvard.edu/abs/2010AJ....140.1868W
  # 306.681, 170.663, 29.0448 and 8.2839 
  # Fnu_0
  vega_norm=np.array([306.681, 170.663, 29.0448, 8.2839]) # in microns

  # F^*_nu0
  # http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4h.html
  # Table 1: column 2
  #vega_norm=np.array([309.540, 171.787, 31.674, 8.363]) # in microns

  #The nominal central wavelengths are 
  # 3.3526, 4.6028, 11.5608, and 22.0883 um for W1,..., W4
  filter_wavelength=np.array([3.3526, 4.6028, 11.5608, 22.0833]) # in microns

  # note the use of numpy log10 and not math.log10
  # Wikipedia
  # Fukugita+1996
  # http://adsabs.harvard.edu/abs/1996AJ....111.1748F
  # 
  AB_flux_normalisation=3631.0

  # Tokunaga, A. T.; Vacca, W. D., 2005
  # http://adsabs.harvard.edu/abs/2005PASP..117..421T
  # Equation 10
  if AB_Tokunaga_2005: AB_flux_normalisation=3720.0

  AB_offset=2.5*np.log10(AB_flux_normalisation/vega_norm)  # 

  if debug or test: 
   print('AB flux normalistation: ', AB_flux_normalisation)
   print('AB offset: ', AB_offset)

# Speed of light
  c = 299792458.0 # m s^-1

# Frequency for each filter; 1e-6 converts the filter 
# central wavelengths to m s^-1
  nu_filter=c/(filter_wavelength*1e-6)

  if debug: 
    print('Debug WISE: ', mag)
    print('Debug WISE: ', waveband)
    print('Debug WISE: ', wavebands)
    print('Debug WISE: ', AB_offset)

  if test:
    result=testit(wavebands, nu_filter, system=system, AB=AB)
    
# do the conversion
  if not test:
    result=convert(mag, waveband, wavebands, AB_offset, nu_filter, AB=AB)

  return result

def testit(wavebands, nu_filter, system='wise', AB=None):
  """


  """

  print('Run tests') 
  print('system= ', system)

  print('Test: Loop throught the wavebands: ', wavebands)
  for (iband, waveband) in enumerate(wavebands):

      waveband_test=wavebands[iband]

      print('Test: ',waveband_test)
      if system == 'sdss':  abmag=sdss(0.0, waveband_test)    
      if system == 'wfcam': abmag=wfcam(0.0, waveband_test)    
      if system == 'wise':  abmag=wise(0.0, waveband_test)    
      
      print('Test: ',waveband_test, '  Vega =   0.0 AB = ', abmag)

      jy=10**(-0.4*abmag)*(3631.0) # Jy
      print('Test: ',waveband_test, 'Flux in Jy: ', jy)

      siflux=10**(-0.4*abmag)*(3631.0*1e-26)
      print('Test: ',waveband_test, 'Flux in SI units (W Hz m^-2): ', siflux)

      nuFnu  = siflux * nu_filter[iband]
      print,('Test: ',waveband_test, 'nuFnu in SI units (W m^-2): ', nuFnu)
      print()

      result=-99.9
   
  print('End of test: Stopping')
  exit  

def main():

  verbose=False
  debug=False

  #sdss(test=True)

  #vista(test=True)

  wise(test=True)
  wfcam(test=True)
  sdss(test=True)

  wise(test=True, AB=True)

  #wise(0.0,'W1',debug=True)


if __name__=='__main__':
  main()
 

