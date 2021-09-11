import os,sys
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
import copy
import numpy as np
from lib.ULS_Engine.SplitMet import *

class Deviation:
    '''
    Compute the maximum deviation possible between two trajectories
    '''

    def __init__(self,A,Er,initSet,T):
        self.A=A # Nominal Dynamics
        self.Er=Er # Perturbations
        self.initialSet=initSet # Initial Set
        self.T=T # Maximum Time Horizon

    def getReachSets(self):
        print(">> STATUS: Computing Reachable Sets . . .")
        time_taken=time.time()
        rs=Split(self.A,self.Er,self.initialSet,self.T)
        (reachORS,reachRS)=rs.getReachableSetAllList()
        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Reachable Sets Computed!")
        return (reachORS,reachRS)
