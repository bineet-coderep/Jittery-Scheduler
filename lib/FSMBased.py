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

    def twoMissesHoldAndSkipAny(self):
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

    def threeMissesHoldAndSkipAny(self):
        '''
        - Three consecutive deadlines allowed.
        - Compute step-wise reachable sets using 'HoldSkipAny' method.
        '''
        uls=ULSGen(self.A,self.B,self.C,self.D,self.K,-10)
        (A_HH, A_MH, A_HM, A_MM)=uls.holdAndSkipAny()
        S0=[self.x0]
        S1=[-1]
        S2=[-1]
        S3=[-1]

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
            if t>3:
                S0_tmp4=StarOp.prodMatStar(A_MH,S3[-1])
            else:
                S0_tmp4=-1

            rsSetTmp=[S0_tmp1,S0_tmp2,S0_tmp3,S0_tmp4]
            rsSet=list(filter(lambda rs: rs!=-1, rsSetTmp))
            s0_t=SetOp.boxHull(rsSet)
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

            # Compute reachable sets for state 3
            if t>2:
                S3_tmp1=StarOp.prodMatStar(A_MM,S2[-1])
                S3.append(copy.copy(S3_tmp1))
            else:
                S3.append(-1)

        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Reachable Sets Computed!")

        return [S0,S1,S2,S3]


class RecRel:

    def __init__(self,automaton,initSet,T,nominalReachSet):
        self.automaton=automaton
        self.initSet=initSet
        self.T=T
        self.nominalReachSet=nominalReachSet

    def getReachSets(self):
        print(">> STATUS: Computing Reachable Sets . . .")
        time_taken=time.time()
        N=self.automaton[0]
        hList=self.automaton[1]
        mList=self.automaton[2]
        stateList=[]

        # Initilize
        state0=[self.initSet]
        stateList.append(copy.copy(state0))
        for k in range(N):
            stateList.append([-1])

        for t in range(1,self.T):
            # Update stateList[0]
            sTmp=[]
            for k in range(N+1):
                if stateList[k][-1]!=-1:
                    sTmp.append(StarOp.prodMatStar(hList[k],stateList[k][-1]))
            if len(sTmp)>1:
                sTmpBox=SetOp.boxHull(sTmp)
            else:
                sTmpBox=copy.copy(sTmp[0])
            stateList[0].append(copy.copy(sTmpBox))

            # Update stateList[k]
            for k in range(1,N+1):
                if t>=k:
                    stateList[k].append(StarOp.prodMatStar(mList[k-1],stateList[k-1][t-1]))
                else:
                    stateList[k].append(-1)

        print("\tTime Taken: ",time.time()-time_taken)
        print(">> STATUS: Reachable Sets Computed!")

        return stateList

    def getDeviations(self,p):
        stateList=self.getReachSets()
        K=len(stateList) # Number of states
        print(">> STATUS: Computing Deviations . . .")
        time_taken=time.time()
        maxD=-7
        maxT=-7
        dList=[0]
        t_max=len(self.nominalReachSet)
        for t in range(1,t_max-1):
            d_t=-7
            for k in range(K):
                if stateList[k][t]!=-1:
                    d_tk=SetOp.getDistance(self.nominalReachSet[t],stateList[k][t],p)
                    if d_tk>d_t:
                        d_t=d_tk
            if d_t>maxD:
                maxD=d_t
                maxT=t
            dList.append(d_t)
        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Deviations Computed!")
        return (stateList,dList,maxT)
