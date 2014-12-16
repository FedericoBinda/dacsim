import numpy as np
from scipy import stats

def apply_pmt(pulse,t,ndynodes=10,delta=4,sigma=5.):
    '''PMT response modeled as gaussian'''

    # histogram the data
    # -------

    hist,bin_edges = np.histogram(pulse,bins=t,range=(t.min(),t.max()))

    # add poisson noise due to electron multiplication statistics
    # -------

    hist *= np.random.poisson(delta,len(hist)) * delta**ndynodes

    # Prepare gaussian response for convolution
    # -------

    dt = t[1]-t[0]
    t2 = np.arange(-3*sigma,3*sigma,dt)
    y = stats.norm.pdf(t2, loc=0, scale=sigma)

    # Convolve pulse with gaussian response
    # -------

    newpulse = np.convolve(hist,y)[:len(t)]
    
    return newpulse
