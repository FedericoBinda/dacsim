'''
Edist
=====

Module that takes care of the energy distribution of the pulses.
'''

import numpy as np
import os

def load_energy_spectrum(which):
    '''Reads the spectrum from the 
    input file "dat/spectrum_<which>.dat".

    Args:
        which (string): particle for which the spectrum has to be loaded (electron, proton)

    Returns:
        energy (numpy.array): energy axis [keVee]

        intensity (numpy.array): normalized spectrum
    
    '''

    # Find the file with coefficients
    # ------

    fname = 'dat/spectrum_' + which + '.dat'

    try:
        mydir = os.path.dirname(__file__)
        cfilename = os.path.join(mydir[:-3], fname)
    except NameError:
        mydir = './src'
        cfilename = os.path.join(mydir[:-4], fname)

    print 'Reading energy spectrum from', cfilename

    # Read the spectrum
    # ------

    try:
        cfile = open(cfilename,'r')
        lines = cfile.readlines()
        cfile.close()
    except IOError:
        print 'File spectrum.dat not found!'
        print 'Continuing without values for the spectrum'
        return
    
    energy = []
    intensity = []

    for line in lines:
        if line[0] == '#':
            continue
        else:
            spl = line.split()
            if len(spl) == 2:
                energy.append(float(spl[0]))
                intensity.append(float(spl[1]))
                          
    energy = np.array(energy)
    intensity = np.array(intensity)
    intensity /= sum(intensity)

    return energy, intensity
