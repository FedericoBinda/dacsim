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
    t, amp = sci.scintillator('proton')
    for i in range(1): # loop for testing speed
        t, phots = sci.generate_pulse(10000,'proton')
    pl.figure(1)
    hist, bins, patches = pl.hist(phots,bins=30,range=(min(t),max(t)))
    pl.figure(2)
    pl.plot(t, amp)
    pl.show()
