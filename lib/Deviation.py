import os,sys
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
import copy
import numpy as np
from lib.ULS_Engine.SplitMet import *
from lib.SetOperations import *

class Deviation:
    '''
    Compute the maximum deviation possible between two trajectories
    '''

    def __init__(self,A,Er,initSet,T,nominalReachSet):
        self.A=A # Nominal Dynamics
        self.Er=Er # Perturbations
        self.initialSet=initSet # Initial Set
        self.T=T # Maximum Time Horizon
        self.nominalReachSet=nominalReachSet

    def getReachSets(self):
        print(">> STATUS: Computing Reachable Sets . . .")
        time_taken=time.time()
        rs=Split(self.A,self.Er,self.initialSet,self.T)
        (reachORS,reachRS)=rs.getReachableSetAllList()
        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Reachable Sets Computed!")
        return (reachORS,reachRS)

    def getDeviations(self,p):
        (reachORS,reachRS)=self.getReachSets()
        print(">> STATUS: Computing Deviations . . .")
        time_taken=time.time()
        maxD=-7
        maxT=-7
        dList=[0]
        t_max=len(self.nominalReachSet)
        for t in range(1,t_max):
            d_t=SetOp.getDistance(self.nominalReachSet[t],reachORS[t],p)
            if d_t>maxD:
                maxD=d_t
                maxT=t
            dList.append(d_t)
        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Deviations Computed!")
        return (reachORS,dList,maxT)
