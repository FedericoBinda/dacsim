import numpy as np
from scipy import stats

def apply_pmt(pulse,t,FWHM=10.):
    '''PMT response modeled as gaussian'''
    hist,bin_edges = np.histogram(pulse,bins=t,range=(t.min(),t.max()))
    dt = t[1]-t[0]
    t2 = np.arange(-5*FWHM,5*FWHM,dt)
    y = stats.norm.pdf(t2, loc=0, scale=FWHM/2.355)
    newpulse = np.convolve(hist,y)[:len(t)]
    return newpulse
