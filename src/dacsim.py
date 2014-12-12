'''
dacsim
======

Data Acquisition Chain Simulation
---------------------------------

Simulate the data acquisition chain of a scintillator:

 - scintillation process
 - photomultiplier tube
 - cable
 - digitizer

'''

import pylab as pl
import sys
from scintillator import *
from pmt import *
from cable import *
from digitize import *

def read_input(fname):
    f = open(fname,'r')
    lines = f.readlines()
    f.close()
    inp_dict = {}
    for line in lines:
        if line[0] == '#':
            continue
        else:
            spl = line.split()
            if len(spl) == 2:
                try:
                    inp_dict[spl[0]] = int(spl[1])
                except:
                    try:
                        inp_dict[spl[0]] = float(spl[1])
                    except:
                        inp_dict[spl[0]] = spl[1]
    return inp_dict

if __name__ == '__main__':
    
    # Read input file
    # ------
    try:
        inp_dict = read_input(sys.argv[1])
    except:
        sys.exit('Missing input file')
    print inp_dict
    
    # Calculate scintillator functions
    # ------
    scint_dict = {}
    t, scint_dict['proton'] = scintillator('proton',dt=inp_dict['dt'],plen=inp_dict['plen'])
    t, scint_dict['electron'] = amp_e = scintillator('electron',dt=inp_dict['dt'],plen=inp_dict['plen'])

    # Generate pulses
    # ------
    nps = inp_dict['nps']
    scint_pulses = generate_pulses(nps,t,scint_dict[inp_dict['ptype']],inp_dict['nphots'])
    pmt_pulses = [ apply_pmt(p,t) for p in scint_pulses ]  
    cable_pulses = [ apply_cable(p, t[:-1]) for p in pmt_pulses ]
    pulses_noise = [ apply_noise(p) for p in cable_pulses ]
    pulses_dig = [ digitize(p,inp_dict['bits'], [inp_dict['minV'],inp_dict['maxV']]) for p in pulses_noise ]

    # Plot first pulse
    # ------
    pl.plot(t[:-1],pulses_dig[0])
    pl.show()
