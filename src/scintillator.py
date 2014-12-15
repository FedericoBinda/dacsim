import os
import numpy as np

def load_coefficients():
    '''
    function that reads the scintillator coefficients from the 
    input file "<dacsim>/dat/scintillator.dat".

     output:
      - parsdict = dictionary with the parameters
    '''

    # Find the file with coefficients
    # ------

    mydir = os.path.dirname(__file__)
    cfilename = os.path.join(mydir[:-3], 'dat/scintillator.dat')
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

coeff_dict = load_coefficients()  

def scintillator(ptype, plen = 600, dt = 0.05):
    '''
    Calculate the scintillator pulse shape.
   
    input:
      - ptype = type of pulse. Can be "electron" or "proton"
      - plen = pulse length [ns]
      - dt = time step [ns]
     output:
      - t = time vector
      - amp = amplitude vector of the scintillation pulse
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

def generate_pulses(n, t, amp, nphots, qeff = 1.):
    '''
    Generate scintillator pulses selcting random times
    according to the scintillator pulse shape.

    input:
      - n = the number of pulses to be generated
      - t = time axis of the scintillator pulse shape
      - amp = amplitude of the scintillator pulse shape
      - nphots = average number of photons in each pulse
      - qeff = quantum efficiency of the PMT. Implemented here
               and not in the pmt module to speed up the calculation
     output:
      - mypulses = list containing the simulated pulses. Each pulse
                   consists of an array of times of photon production
    '''
    
    # Randomize nphots according to poisson distribution and
    # including the quantum efficiency qeff
    # ------

    mynphots = np.random.poisson(nphots*qeff, n)

    # Generate the pulses list
    # ------

    mypulses = [np.random.choice(t, numphots, p = amp) for numphots in mynphots]
    return mypulses
    

