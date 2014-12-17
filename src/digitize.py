'''
Digitize
========

module with the function that takes care of the digitization of the pulse

'''

import numpy as np

def digitize(pulse, t, nbits=8, amprange=[-1.,1], sampfreq = 0.5):
    '''Digitize the signal

    Args:
        pulse (numpy.array): the input signal
        t (numpy.array): the time axis

    Kwargs:
        nbits (int): resolution of the digitizer [bit]
        amprange (list): amplitude range of the digitizer [max,min] [V]
        sampfreq (float): sampling frequency of the digitizer [GHz]

    Returns:
        newpulse (numpy.array): digitized pulse
        newt (numpy.array): time axis of the digitized pulse

    '''

    dt = t[1] - t[0]
    freq = 1. / dt
    ratio = int(freq / sampfreq)
    
    codes = np.linspace(amprange[0],amprange[1],2**nbits)
    newpulse = np.digitize(pulse, codes)[::ratio]
    newt = t[::ratio]
    return newpulse, newt
    
