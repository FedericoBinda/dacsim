import numpy as np
import os

def get_cable_database():
    
    # Find the database file
    # ------

    mydir = os.path.dirname(__file__)
    cfilename = os.path.join(mydir[:-3], 'dat/cable.dat')
    print 'Reading cable database', cfilename

    # Read the parameters
    # ------
    
    cable_dict = {}


    # temporary. implement proper database
    cable_dict['RG58'] = np.array([[1,5,15,20,25,50],[0.05,0.2,1.0,3.3,8.0,30.0]]) 

    return cable_dict

cable_dict = get_cable_database()

def apply_cable(signal, t, cable_length = 1, cable_type = 'RG58'):
    try:
        mask = (cable_dict[cable_type][0] == cable_length)
    except KeyError:
        print 'ERROR! cable type not present in database!'
        return 0
    if True not in mask: # NOTE: implement interpolation of length
        print 'ERROR! cable length not present in database!'
        return 0
    print cable_dict[cable_type][1][mask]
    tau = cable_dict[cable_type][1][mask][0]
    cable_effect = np.exp(-t/tau)
    return np.convolve(cable_effect, signal, 'same')
