import numpy as np

def apply_pmt(pulse,t,tau=10.):
    hist,bin_edges = np.histogram(pulse,bins=t,range=(t.min(),t.max()))
    return hist*(1 - np.exp(-t[:-1]/tau))
