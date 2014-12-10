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
    t, amp_p = sci.scintillator('proton')
    t, amp_e = sci.scintillator('electron')
    mypulses = sci.generate_pulses(10000,t,amp_p,10000)
    phots = mypulses[0]
    pl.figure(1)
    hist, bins, patches = pl.hist(phots,bins=30,range=(min(t),max(t)))
    pl.figure(2)
    pl.plot(t, amp_p)
    pl.plot(t, amp_e)
    pl.show()
