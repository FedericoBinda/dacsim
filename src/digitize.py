'''
Digitize
========

module with the function that takes care of the digitization of the pulse

'''

import numpy as np

def digitize(pulse, t, nbits=8, amprange=[-1.,1], sampfreq = 0.5, samples = 256, do_threshold = False, threshold = 50, pretriggersamples = 64,noise = 0.02):
    '''Digitize the signal

    Args:
        pulse (numpy.array): the input signal

        t (numpy.array): the time axis

    Kwargs:
        nbits (int): resolution of the digitizer [bit]

        amprange (list): amplitude range of the digitizer [max,min] [V]

        sampfreq (float): sampling frequency of the digitizer [GHz]

        samples = number of samples to acquire

        do_threshold (bool): activate trigger threshold effect
        
        threshold (int): level of trigger threshold (starting from baseline value)

        pretriggersamples (int): number of samples before the trigger

        noise (float): noise level [mV]

    Returns:
        newpulse (numpy.array): digitized pulse

    '''

    dt = t[1] - t[0]
    freq = 1. / dt
    ratio = int(freq / sampfreq)
    
    codes = np.linspace(amprange[0],amprange[1],2**nbits)
    dV = (amprange[1] - amprange[0]) / 2**nbits
    th_V = threshold * dV

    if do_threshold:
        try:
            trigger = np.where(pulse >= th_V)[0][0]
        except IndexError:
            return
        pretrig = pulse[trigger::-ratio][::-1]
        diff = pretriggersamples - len(pretrig)
        if diff < 0:
            pretrig = pretrig[-diff:]
        elif diff > 0:
            to_append = np.random.normal(0,noise,diff)
            pretrig = np.append(to_append,pretrig)
        newpulse = np.append(pretrig,pulse[trigger+ratio::ratio])

        diff2 = samples - len(newpulse)
        if diff2 < 0:
            newpulse = newpulse[:samples]
        elif diff2 > 0:
            to_append = np.random.normal(0,noise,diff2)
            newpulse = np.append(newpulse,to_append)
    else:
        newpulse = pulse[::ratio]

    newpulse = np.digitize(newpulse, codes)

    return newpulse
    
