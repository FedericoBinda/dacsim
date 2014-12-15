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

Input file
----------

The code reads an input file in which the following variables MUST be defined:

nps: the number of pulses to be simulated
dt: the time step for the simulated pulses [ns]
plen: the length of each pulse [ns]
qeff: the quantum efficiency of the photomultiplier tube
ptype: the type of particle that deposited energy in the scintillator (electron, proton)
nphots: the average number of photons produced by each particle interaction
bits: the number of bits of the digitizer
minV: the minimum input level of the digitizer [a.u.]
maxV: the maximum input level of the digitizer [a.u.]
cutoff: the frequency cutoff of the cable [GHz]
noise: the noise level [a.u.]
output: the name of the output file (no extension)

an example input file:

nps 1
dt 0.05
plen 600
qeff 0.26
ptype electron
nphots 10000
bits 14
minV -10
maxV 10
cutoff 0.2
noise 0.01
output myout

Output
------

The codes generates a subdirectory called 'output' (if it does not exist) in
the current directory and saves an output file with the name defined in the input
and extension '.npy'.
The file contains the list of the generated pulses.
For information on how to read the file refer to the numpy.load function
'''

import pylab as pl
import sys
from scintillator import *
from pmt import *
from cable import *
from digitize import *

def save_output(pulses,fname):
    dirpath = os.getcwd() + '/output/'
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    outfname = dirpath + fname
    np.save(outfname, pulses)

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
    scint_pulses = generate_pulses(nps,t,scint_dict[inp_dict['ptype']],inp_dict['nphots'], inp_dict['qeff'])
    pmt_pulses = [ apply_pmt(p,t) for p in scint_pulses ]  
    cable_pulses = [ apply_cable(p, t[:-1],inp_dict['cutoff']) for p in pmt_pulses ]
    pulses_noise = [ apply_noise(p,inp_dict['noise']) for p in cable_pulses ]
    pulses_dig = [ digitize(p,inp_dict['bits'], [inp_dict['minV'],inp_dict['maxV']]) for p in pulses_noise ]

    # Save pulses
    # ------

    save_output(pulses_dig,inp_dict['output'])

    # Plot first pulse
    # ------
    pl.plot(t[:-1],pulses_dig[0])
    pl.show()
