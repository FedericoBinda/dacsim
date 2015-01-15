'''
Scintillator
============

module with scintillator functions
'''

import os
import numpy as np

def load_coefficients():
    '''Reads the scintillator coefficients from the 
    input file "dat/scintillator.dat".

    Returns:
        parsdict (dict): dictionary with the parameters
    
    '''

    # Find the file with coefficients
    # ------

    try:
        mydir = os.path.dirname(__file__)
        cfilename = os.path.join(mydir[:-3], 'dat/scintillator.dat')
        print cfilename
    except NameError:
        mydir = './src'
        cfilename = os.path.join(mydir[:-4], 'dat/scintillator.dat')

    print 'Reading scintillator parameters from', cfilename

    # Read the parameters
    # ------

    coeff_dict = {}

    try:
        cfile = open(cfilename,'r')
        lines = cfile.readlines()
        cfile.close()
    except IOError:
        print 'File scintillator.dat not found!'
        print 'Continuing without values for the scintillator parameters'
        return coeff_dict
    
    now = ''

    for line in lines:
        if line[0] == '#':
            continue
        else:
            spl = line.split()
            if len(spl) == 1:
                now = spl[0]
                coeff_dict[now] = []
            if len(spl) == 2:
                coeff_dict[now].append(map(float,spl))
    return coeff_dict

def scintillator(ptype, coeff_dict, plen = 600, dt = 0.05):
    '''Calculates the scintillator pulse shape.
    
    Args:
        ptype (str): type of pulse. Can be "electron" or "proton"
        coeff_dict (dict): dictionary with scintillator coefficients

    Kwargs:
        plen (float): pulse length [ns]
        dt (float): time step [ns]
    
    Returns:
        t (numpy.array): time vector
        amp (numpy.array): amplitude vector of the scintillation pulse

    '''

    t = np.arange(0,plen,dt) # time axis
    try:
        amp = [ (c[1])*np.exp(-t/c[0]) for c in coeff_dict[ptype] ]
        amp = sum(amp)
        amp = amp / sum(amp) # normalization
        return t, amp
    except KeyError:
        print 'ERROR! ptype not valid!'
        return 0

def generate_pulses(n, t, amp, energy, spectrum, k = 10., lc = 1., qeff = 1.):
    '''Generates scintillator pulses selcting random times
    according to the scintillator pulse shape.
    
    Args:
        n (int): the number of pulses to be generated
        t (numpy.array): time axis of the scintillator pulse shape
        amp (numpy.array): amplitude of the scintillator pulse shape
        nphots (int): average number of photons in each pulse

    Kwargs:
        qeff (float): quantum efficiency of the PMT. Implemented here
        and not in the pmt module to speed up the calculation
    
    Returns:
        mypulses (list): list containing the simulated pulses. Each pulse
        consists of an array of times of photon production
    
    '''
    
    # Convert energy axis to nphots axis
    # ------

    nphots_axis = energy * k

    # Generate nphots spectrum
    # ------

    nphots = np.random.choice(nphots_axis, n, p = spectrum)

    # Randomize nphots according to poisson distribution and
    # including the quantum efficiency qeff and 
    # the light collection efficiency lc
    # ------

    mynphots = np.random.poisson(nphots*qeff, n)

    # Generate the pulses list
    # ------

    mypulses = [np.random.choice(t, numphots, p = amp) for numphots in mynphots]
    return mypulses
    

