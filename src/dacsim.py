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
import pmt

if __name__ == '__main__':
    t, amp_p = sci.scintillator('proton')
    t, amp_e = sci.scintillator('electron')
    mypulses = sci.generate_pulses(1000,t,amp_p,10000)
    phots = mypulses[0]
    pl.figure(1)
    hist, bins, patches = pl.hist(phots,bins=t,range=(min(t),max(t)))
    newhist=pmt.apply_pmt(mypulses[0],t)
    pl.plot(t[:-1],newhist)
    pl.figure(2)
    pl.plot(t, amp_p)
    pl.plot(t, amp_e)
    pl.show()
