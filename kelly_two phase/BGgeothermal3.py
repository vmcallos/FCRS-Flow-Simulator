# About this version: modified to include provision for wells in shut condition

from t2thermo import *
from t2thermo_rnc import *

class WellClass(object):
    ''' I want this to access the BOC equations, calculate the two-phase mass flow and enthalpy of the fluid from the well and lastly, to tap the separator vessel'''
    def __init__(self, whp, mf1, mf2, mf3, mf4, mf5, mf6, h1, h2, h3, h4, h5):
        self.owhp = whp
        #print(self.owhp)
        self.mf1 = mf1
        self.mf2 = mf2
        self.mf3 = mf3
        self.mf4 = mf4
        self.mf5 = mf5
        self.mf6 = mf6
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.h5 = h5

    def massflow(self):
        #print(self.owhp)
        if self.owhp == 'SHUT':
            self.massflow = 0.0
        else:
            self.massflow = self.mf1 + (self.mf2 * self.owhp) + (self.mf3 * self.owhp**2) + (self.mf4 * self.owhp**3) + (self.mf5 * self.owhp**4) + (self.mf6 * self.owhp**5)
        return self.massflow

    def enthalpy(self):
        if self.owhp == 'SHUT':
            self.enthalpy = 0.0
        else:
            self.enthalpy = self.h1 + (self.h2 * self.owhp) + (self.h3 * self.owhp**2) + (self.h4 * self.owhp**3) + (self.h5 * self.owhp**4)
        return self.enthalpy

class VesselClass(object):
    def __init__(self, separatorPressure,opening):
        self.sepP = separatorPressure
        self.open = opening

def Enthliq(p):
    '''Enter pressure in MPag'''
    hf, hg = Enthalpy(p*1e6)
    return hf

def Enthgas(p):
    '''Enter pressure in MPag'''
    hf, hg = Enthalpy(p*1e6)
    return hg



