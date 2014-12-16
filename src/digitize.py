import numpy as np

def digitize(pulse, nbits=8, amprange=[-1.,1]):
    codes = np.linspace(amprange[0],amprange[1],2**nbits)
    return np.digitize(pulse, codes)
    
