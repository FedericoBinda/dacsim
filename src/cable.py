'''
Cable
=====

module with cable filtering function and noise
'''

import numpy as np
from scipy import signal

def apply_cable(pulse, t, cutoff = 0.1, impedance = 50):
    '''Cable effect modeled as a lowpass filter

    Args:
        pulse (numpy.array): input pulse from pmt
        t (numpy.array): time axis of the pulse

    Kwargs:
        cutoff (float): cutoff of the filter [GHz]
        impedance (float): impedance of the cable [ohm]

    Returns:
        newpulse (numpy.array): filtered pulse [V]

    '''
    sampling_freq = 1./(t[1]-t[0]) # GHz
    Wn = (1./(2*np.pi))*(cutoff/sampling_freq)
    b, a = signal.butter(1, Wn, 'low')
    newpulse = signal.lfilter(b,a,pulse) * impedance
    return newpulse

def apply_noise(pulse, level = 0.02):
    '''Add electric noise (gaussian oscillation) to the pulse

    Args:
        pulse (numpy.array): input pulse

    Kwargs:
        level (float): the amount of noise [V]

    Returns:
        newpulse (numpy.array): pulse with noise [V]

    '''
    noise = np.random.normal(0,level,len(pulse))
    newpulse = pulse + noise
    return newpulse
    
