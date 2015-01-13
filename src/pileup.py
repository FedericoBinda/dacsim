'''
Pileup
======

module that simulates pileup effects
'''

import numpy as np

def ApplyPileup(n,rate,plen,baseline):
    dt_array = np.random.exponential(rate,n-1)
    i_pileup = np.where(dt_array < plen)
    dt_array = np.append(np.array([0]),dt_array)
    trig_t = np.cumsum(dt_array)
    
