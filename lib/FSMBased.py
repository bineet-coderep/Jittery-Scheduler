import os,sys
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
import copy
import numpy as np
from lib.ULSGenerator import *
from lib.StarOperations import *
from lib.SetOperations import *
import time

class FSM:

    def __init__(self,A,B,C,D,K,x0,T):
        self.A=A # Dynamics
        self.B=B # Dynamics
        self.C=C # Dynamics
        self.D=D # Dynamics
        self.K=K # Control
        self.x0=x0 # Initial Set
        self.T=T # Time Bound

    def twoMissesholdAndSkipAny(self):
        '''
        - Two consecutive deadlines allowed.
        - Compute step-wise reachable sets using 'HoldSkipAny' method.
        '''

        uls=ULSGen(self.A,self.B,self.C,self.D,self.K,-10)
        (A_HH, A_MH, A_HM, A_MM)=uls.holdAndSkipAny()
        S0=[self.x0]
        S1=[-1]
        S2=[-1]

        print(">> STATUS: Computing Reachable Sets . . .")
        time_taken=time.time()

        for t in range(1,self.T+1):
            # Compute reachable sets for state 0
            S0_tmp1=StarOp.prodMatStar(A_HH,S0[-1])
            if t>1:
                S0_tmp2=StarOp.prodMatStar(A_MH,S1[-1])
            else:
                S0_tmp2=-1
            if t>2:
                S0_tmp3=StarOp.prodMatStar(A_MH,S2[-1])
            else:
                S0_tmp3=-1

            if S0_tmp2!=-1 and S0_tmp3!=-1:
                s0_t=SetOp.boxHull([S0_tmp1,S0_tmp2,S0_tmp3])
            elif S0_tmp2!=-1 and S0_tmp3==-1:
                s0_t=SetOp.boxHull([S0_tmp1,S0_tmp2])
            else:
                s0_t=copy.copy(S0_tmp1)
            S0.append(copy.copy(s0_t))

            # Compute reachable sets for state 1
            S1_tmp1=StarOp.prodMatStar(A_HM,S0[-1])
            S1.append(copy.copy(S1_tmp1))

            # Compute reachable sets for state 2
            if t>1:
                S2_tmp1=StarOp.prodMatStar(A_MM,S1[-1])
                S2.append(copy.copy(S2_tmp1))
            else:
                S2.append(-1)

        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Reachable Sets Computed!")

        return [S0,S1,S2]
