import numpy as np
from scipy import signal
import os

def get_cable_database():
    
    # Find the database file
    # ------

    mydir = os.path.dirname(__file__)
    cfilename = os.path.join(mydir[:-3], 'dat/cable.dat')
    print 'Reading cable database', cfilename

    # Read the parameters
    # ------
    
    cable_dict = {}


    # temporary. implement proper database
    cable_dict['RG58'] = np.array([[1,5,15,20,25,50],[0.05,0.2,1.0,3.3,8.0,30.0]]) 

    return cable_dict

cable_dict = get_cable_database()

def apply_cable(pulse, t, cutoff = 0.1):

    sampling_freq = 1./(t[1]-t[0]) # GHz
    Wn = (1./(2*np.pi))*(cutoff/sampling_freq)
    b, a = signal.butter(1, Wn, 'low')
    return signal.lfilter(b,a,pulse)
