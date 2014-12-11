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
import cable

if __name__ == '__main__':
    dt = 0.5
    t, amp_p = sci.scintillator('proton',dt=dt)
    t, amp_e = sci.scintillator('electron',dt=dt)
    mypulses = sci.generate_pulses(1,t,amp_p,10000)
    phots = mypulses[0]
    pl.figure(1) # scintillator
    hist, bins, patches = pl.hist(phots,bins=t,range=(min(t),max(t)))
    pl.figure(2) # pmt
    newhist=pmt.apply_pmt(mypulses[0],t)
    pl.plot(t[:-1],newhist)
    pl.figure(3) # cable
    new_y = cable.apply_cable(newhist, t[:-1])
    pl.plot(t[:-1],new_y)
    pl.figure(4) # noise
    wnoise = cable.apply_noise(new_y)
    pl.plot(t[:-1],wnoise)
    #pl.plot(t, amp_p)
    #pl.plot(t, amp_e)
    pl.show()
