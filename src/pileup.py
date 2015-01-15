'''
Pileup
======

module that simulates pile-up effects
'''

import numpy as np

def apply_pileup(plist,rate,plen):
    '''Applies pile-up to the scintillator pulses.

    Args:
        plist (list): the list of scintillator pulses.
        rate (float): the total count rate
        plen (float): pulse length [ns]

    Returns:
        plist (list): the list of scintillator pulses with pileup.

    '''
    if type(plist) == np.ndarray:
        plist = list(plist)
    n = len(plist)
    tint_array = np.random.exponential(1./rate,n-1) # time intervals
    i = 0
    t_0 = 0
    for tint in tint_array:
        if (tint + t_0) < plen*1e-9:
            plist[i] = np.append(plist[i],plist[i+1]+(tint+t_0)*1e9)
            del plist[i+1]
            t_0 += tint
        else:
            i += 1
            t_0 = 0
    return plist
