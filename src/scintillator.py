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

def scintillator(ptype, plen = 600, dt = 2.5):
    '''
    Generate a scintillator pulse.
   
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

def generate_pulses(n, t, amp, nphots):
    mypulses = [np.random.choice(t, nphots, p = amp) for i in range(n)]
    return mypulses
    

