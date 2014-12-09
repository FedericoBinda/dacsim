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
import scintillator as sci

if __name__ == '__main__':
    t, amp = sci.scintillator(1,'proton')
    pl.plot(t, amp)
    pl.show()
