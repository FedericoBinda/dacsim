import numpy as np

def apply_pmt(pulse,t,tau=3.):
    '''PMT modeled as a RC circuit with time constat tau'''
    hist,bin_edges = np.histogram(pulse,bins=t,range=(t.min(),t.max()))
    return hist*(1 - np.exp(-t[:-1]/tau))
