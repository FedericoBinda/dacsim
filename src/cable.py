import numpy as np
from scipy import signal

def get_cable_database():
    
    # Find the database file
    # ------

    mydir = os.path.dirname(__file__)
    cfilename = os.path.join(mydir[:-3], 'dat/cable.dat')
    print 'Reading cable database', cfilename

    # Read the parameters
    # ------
    
    cable_dict = {}



    cable_dict['RG58'] = [50] # temporary. implement proper database
    return cable_dict

cable_dict = get_cable_database()

def apply_cable(signal, t, cable_length = 10, cable_type = 'RG58'):
    
