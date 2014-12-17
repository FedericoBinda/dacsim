'''
dacsim
======

Data Acquisition Chain Simulation
---------------------------------

Simulate the data acquisition chain of a scintillator.
The following parts of the acquosition chain are modeled:

 - scintillation process
 - photomultiplier tube
 - cable
 - digitizer

Input file
----------

The code reads an input file in which the following variables MUST be defined:

 - nps: the number of pulses to be simulated
 - ptype: the type of particle that deposited energy in the scintillator (electron, proton)
 - output: the name of the output file (no extension)
 - dt: the time step for the simulated pulses [ns]
 - plen: the length of each pulse [ns]
 - qeff: the quantum efficiency of the photomultiplier tube
 - nphots: the average number of photons produced by each particle interaction
 - ndyn: the number of dynodes in the pmt
 - delta: the average gain of the dynodes
 - sigma: the broadening of the pmt response
 - tt: the transit time of the pmt
 - cutoff: the frequency cutoff of the cable [GHz]
 - imp: the impedance of the cable [ohm]
 - noise: the noise level [V]
 - bits: the number of bits of the digitizer
 - minV: the minimum input level of the digitizer [V]
 - maxV: the maximum input level of the digitizer [V]
 - sampf: the sampling frequency of the digitizer [GHz]
 - fp: if 1, plot the first simulated pulse

example input file::
    
    # input example for dacsim
    # this line is a comment
    
    # general parameters
    
    nps 10
    ptype electron
    output myout
    
    # scintillator parameters
    
    dt 0.05
    plen 800
    qeff 0.26
    nphots 10000
    
    # pmt parameters
    
    ndyn 10
    delta 4
    sigma 5.2
    tt 17.5
    
    # cable parameters
    
    cutoff 0.2
    imp 50
    noise 0.01
    
    # digitizer parameters
    
    bits 12
    minV -0.1
    maxV 1.2
    sampf 0.4

    # plotting parameters

    fp 1


Output
------

The codes generates a subdirectory called 'output' (if it does not exist) in
the current directory and saves an output file with the name defined in the input
and extension '.npy'.
The output format is:
[t_dig,[p_1,p_2,...,p_nps]]
where t_dig is the digitized time axis and p_1,p_2,..,p_nps are the digitized pulses.
For information on how to read the file refer to the 
`numpy.load <http://docs.scipy.org/doc/numpy/reference/generated/numpy.load.html>`_ function

'''

import pylab as pl
import sys
from scintillator import *
from pmt import *
from cable import *
from digitize import *

def save_output(pulses,fname):
    '''Saves the output file
    
    Args:
        pulses (list): list of simulated pulses
        fname (str): name of the output file
    '''
    dirpath = os.getcwd() + '/output/'
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    outfname = dirpath + fname
    np.save(outfname, pulses)

def read_input(fname):
    '''Reads the input file and saves the parameters into a dictionary

    Args:
        fname (str): name of the input file

    Returns:
        inp_dict (dict): dictionary with the input parameters
    '''
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
    pmt_pulses = [ apply_pmt(p,t,inp_dict['ndyn'],inp_dict['delta'],inp_dict['sigma'],inp_dict['tt']) for p in scint_pulses ]  
    cable_pulses = [ apply_cable(p,t,inp_dict['cutoff'],inp_dict['imp']) for p in pmt_pulses ]
    pulses_noise = [ apply_noise(p,inp_dict['noise']) for p in cable_pulses ]
    pulses_dig = [ digitize(p,t,inp_dict['bits'], [inp_dict['minV'],inp_dict['maxV']],inp_dict['sampf']) for p in pulses_noise ]
    t_dig = get_digitized_time(t,inp_dict['sampf'])

    # Save pulses
    # ------

    save_output([t_dig,pulses_dig],inp_dict['output'])

    # Plot first pulse
    # ------
    
    if inp_dict['fp'] == 1:

        pl.plot(t_dig,pulses_dig[0])
        pl.show()
