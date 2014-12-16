'''
Pmt
===

module with the photomultiplier response function
'''

import numpy as np
from scipy import stats, constants


def apply_pmt(pulse,t,ndynodes=10,delta=4,sigma=5.):
    '''Adds the pmt response to a signal. 
    The pmt response is modeled as a gaussian with amplitude depending on the
    number of dynodes and the dynode gain.

    Args:
        pulse (numpy.array): the photon pulse from the scintillator
        t (numpy.array): the time axis of the pulse

    Kwargs:
        ndynodes (int): the number of  dynodes
        delta (float): the average gain of the dynodes
        sigma (float): the time spread of the gaussian response [ns]

    Returns:
        newpulse (numpy.array): the current pulse produced by the pmt

    '''

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

    # Convert the pulse from n_electrons to current
    # -----
    
    newpulse *= constants.e / (dt*1.e-9)

    return newpulse
