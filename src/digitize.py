'''
Digitize
========

module with the function that takes care of the digitization of the pulse

'''

import numpy as np
from cable import apply_noise

def get_digitized_time(t, sampfreq = 0.5):
    '''Get the digitized time axis

    Args:
        t (numpy.array): the original time axis

    Kwargs:
        sampfreq (float): sampling frequency of the digitizer [GHz]

    Returns:
        newt (numpy.array): time axis of the digitized pulse

    '''

    dt = t[1] - t[0]
    freq = 1. / dt
    ratio = int(freq / sampfreq)

    newt = t[::ratio]
    return newt

def digitize(pulse, t, nbits=8, amprange=[-1.,1], sampfreq = 0.5, do_threshold = False, threshold = 50, pretriggersamples = 64, noise = 0.02):
    '''Digitize the signal

    Args:
        pulse (numpy.array): the input signal

        t (numpy.array): the time axis

    Kwargs:
        nbits (int): resolution of the digitizer [bit]

        amprange (list): amplitude range of the digitizer [max,min] [V]

        sampfreq (float): sampling frequency of the digitizer [GHz]

        do_threshold (bool): activate trigger threshold effect
        
        threshold (int): level of trigger threshold (starting from baseline value)

        pretriggersamples (int): number of samples before the trigger

        mnoise (float): noise level [mV]

    Returns:
        newpulse (numpy.array): digitized pulse

    '''

    dt = t[1] - t[0]
    freq = 1. / dt
    ratio = int(freq / sampfreq)
    
    codes = np.linspace(amprange[0],amprange[1],2**nbits)
        
    newpulse = np.digitize(pulse, codes)

    if do_threshold:
        baseline = -amprange[0]*2**nbits/(amprange[1]-amprange[0])
        if max(newpulse) < baseline+threshold:
            return
        trigger = np.where(newpulse > baseline+threshold)[0][0]
        pretrig = newpulse[trigger::-ratio][::-1]
        diff = pretriggersamples - len(pretrig)
        if diff < 0:
            pretrig = pretrig[-diff:]
        elif diff > 0:
            pretrig = np.append(np.random.normal(0,noise,diff),pretrig)
        newpulse = np.append(pretrig,newpulse[trigger+ratio::ratio]
        
    else:
        newpulse = newpulse[::ratio]
    
    return newpulse
    
