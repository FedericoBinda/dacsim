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

def scintillator(t,ptype):
    '''
    Scintillator pulse function.
   
    input:
      - t = time
      - ptype = type of pulse. Can be "electron" or "proton"
     output:
      - amp = amplitude of the scintillation pulse
    '''
    return 0
