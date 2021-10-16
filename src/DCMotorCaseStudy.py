'''
This is to generate results for the draft
'''

import os,sys
import random,numpy
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from lib.Benchmarks import *
from lib.Visualization import *
from lib.ULSGenerator import *
from lib.Deviation import *
from lib.LQRSolver import *
from lib.BoundedTree import *
from lib.FSMBased import *
import time

class ULSBased:

    def holdAndKill():
        '''
        - Applies Hold&Kill scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - All possible sequences of hit/miss
        '''
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        MAX_DEADLINE=-1 # Any
        methodName="HoldKill"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: ULS.\tPolicy: ",methodName,".")
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldKill(initialSet,nominalSeqn)

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,MAX_DEADLINE,methodName)
        uncertainMat=ulsGen.getUncertainMatrix()

        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T,nominalReachSet)
        (reachORS,dList,maxT)=deviation.getDeviations(p)

        print("\tMax Deviation: ",dList[maxT],";\t At time step: ",maxT)
        print("\tTotal Time Taken: ",time.time()-time_taken)
        print(">> End of Report!")
        #VizRS.vizDevs(dList,maxT)

        return (dList,maxT)

    def zeroAndKill():
        '''
        - Applies Zero&Kill scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - All possible sequences of hit/miss
        '''
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        MAX_DEADLINE=-1 # Any
        methodName="ZeroKill"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: ULS.\tPolicy: ",methodName,".")
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetZeroKill(initialSet,nominalSeqn)

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,MAX_DEADLINE,methodName)
        uncertainMat=ulsGen.getUncertainMatrix()

        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T,nominalReachSet)
        (reachORS,dList,maxT)=deviation.getDeviations(p)

        print("\tMax Deviation: ",dList[maxT],";\t At time step: ",maxT)
        print("\tTotal Time Taken: ",time.time()-time_taken)
        print(">> End of Report!")
        #VizRS.vizDevs(dList,maxT)

        return (dList,maxT)

    def holdAndSkip():
        '''
        - Applies Hold&Skip scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - 3 consecutive misses allowed
        '''
        C_nom=[0]*3
        V_nom=np.zeros((3,3))
        V_nom[0][0]=1.0
        V_nom[1][1]=1.0
        P_nom=[(10,10),(10,10)]
        P_nom=P_nom+[(0,0)]*1
        initialSet_nom=(C_nom,V_nom,P_nom)

        C=[0]*9
        V=np.zeros((9,9))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(0,0)]*7
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        MAX_DEADLINE=3 # Three
        methodName="HoldSkip"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: ULS.\tPolicy: ",methodName,".")
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldSkip(initialSet_nom,nominalSeqn)

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,MAX_DEADLINE,methodName)
        uncertainMat=ulsGen.getUncertainMatrix()

        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T,nominalReachSet)
        (reachORS,dList,maxT)=deviation.getDeviations(p)

        print("\tMax Deviation: ",dList[maxT],";\t At time step: ",maxT)
        print("\tTotal Time Taken: ",time.time()-time_taken)
        print(">> End of Report!")
        #VizRS.vizDevs(dList,maxT)

        return (dList,maxT)

    def holdAndSkipAny():
        '''
        - Applies Hold&Skip scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - All possible sequences of hit/miss
        '''

        C=[0]*5
        V=np.zeros((5,5))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(0,0)]*5
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        MAX_DEADLINE=-1 # Any
        methodName="HoldSkipAny"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: ULS.\tPolicy: ",methodName,".")
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldSkipAny(initialSet,nominalSeqn)

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,MAX_DEADLINE,methodName)
        uncertainMat=ulsGen.getUncertainMatrix()

        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T,nominalReachSet)
        (reachORS,dList,maxT)=deviation.getDeviations(p)

        print("\tMax Deviation: ",dList[maxT],";\t At time step: ",maxT)
        print("\tTotal Time Taken: ",time.time()-time_taken)
        print(">> End of Report!")
        #VizRS.vizDevs(dList,maxT)

        return (dList,maxT)

    def allPolicies():
        '''
        Initial Set: [[10,10],[10,10]]
        '''
        (dList_HK,maxT_HK)=ULSBased.holdAndKill() # Any number of miss
        print("\n-----------\n")
        (dList_ZK,maxT_ZK)=ULSBased.zeroAndKill() # Any number of miss
        print("\n-----------\n")
        (dList_HS,maxT_HS)=ULSBased.holdAndSkip() # 3 consecutive misses
        print("\n-----------\n")
        (dList_HSA,maxT_HSA)=ULSBased.holdAndSkipAny() # Any number of miss
        print("\n-----------\n")

        labels=["HoldKill","ZeroKill"]
        allDevLists=[dList_HK,dList_ZK]
        maxTLists=[maxT_HK,maxT_ZK]

        VizRS.vizAllDevs(labels,allDevLists,maxTLists,"dc_motor_uls")


class FSMBased:

    def holdAndKill():
        '''
        - Applies Hold&Kill scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        MAX_DEADLINE=3
        methodName="HoldKill"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: Recurrence Relation.\tPolicy: ",methodName,".\tMax Deadline Miss: ",MAX_DEADLINE)
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldKill(initialSet,nominalSeqn)

        # Get the matrices
        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,MAX_DEADLINE,methodName)
        matList=ulsGen.getAllPossibleMatrices()

        hList=[matList[0]]*(MAX_DEADLINE+1)
        mList=[matList[1]]*MAX_DEADLINE

        automaton=(MAX_DEADLINE,hList,mList)

        rec=RecRel(automaton,initialSet,T,nominalReachSet)
        stateList,dList,maxT=rec.getDeviations(p)

        print("\tMax Deviation: ",dList[maxT],";\t At time step: ",maxT)
        print("\tTotal Time Taken: ",time.time()-time_taken)
        print(">> End of Report!")
        #VizRS.vizDevs(dList,maxT)
        return (dList,maxT)

    def zeroAndKill():
        '''
        - Applies Zero&Kill scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        MAX_DEADLINE=3
        methodName="ZeroKill"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: Recurrence Relation.\tPolicy: ",methodName,".\tMax Deadline Miss: ",MAX_DEADLINE)
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetZeroKill(initialSet,nominalSeqn)

        # Get the matrices
        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,MAX_DEADLINE,methodName)
        matList=ulsGen.getAllPossibleMatrices()

        hList=[matList[0]]*(MAX_DEADLINE+1)
        mList=[matList[1]]*MAX_DEADLINE

        automaton=(MAX_DEADLINE,hList,mList)

        rec=RecRel(automaton,initialSet,T,nominalReachSet)
        stateList,dList,maxT=rec.getDeviations(p)

        print("\tMax Deviation: ",dList[maxT],";\t At time step: ",maxT)
        print("\tTotal Time Taken: ",time.time()-time_taken)
        print(">> End of Report!")
        #VizRS.vizDevs(dList,maxT)
        return (dList,maxT)

    def holdAndSkip():
        '''
        - Applies Hold&Skip scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''
        C_nom=[0]*3
        V_nom=np.zeros((3,3))
        V_nom[0][0]=1.0
        V_nom[1][1]=1.0
        P_nom=[(10,10),(10,10)]
        P_nom=P_nom+[(0,0)]*1
        initialSet_nom=(C_nom,V_nom,P_nom)

        C=[0]*9
        V=np.zeros((9,9))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(0,0)]*7
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        MAX_DEADLINE=3
        methodName="HoldSkip"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: Recurrence Relation.\tPolicy: ",methodName,".\tMax Deadline Miss: ",MAX_DEADLINE)
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldSkip(initialSet_nom,nominalSeqn)

        # Get the matrices
        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,MAX_DEADLINE,methodName)
        matList=ulsGen.getAllPossibleMatrices()

        hList=copy.copy(matList[1:])
        mList=[matList[0]]*MAX_DEADLINE

        automaton=(MAX_DEADLINE,hList,mList)

        rec=RecRel(automaton,initialSet,T,nominalReachSet)
        stateList,dList,maxT=rec.getDeviations(p)

        print("\tMax Deviation: ",dList[maxT],";\t At time step: ",maxT)
        print("\tTotal Time Taken: ",time.time()-time_taken)
        print(">> End of Report!")
        #VizRS.vizDevs(dList,maxT)
        return (dList,maxT)

    def holdAndSkipAny(MAX_DEADLINE=3):
        '''
        - Applies Hold&SkipAny scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''

        C=[0]*5
        V=np.zeros((5,5))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(0,0)]*3
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        methodName="HoldSkipAny"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: Recurrence Relation.\tPolicy: ",methodName,".\tMax Deadline Miss: ",MAX_DEADLINE)
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldSkipAny(initialSet,nominalSeqn)

        # Get the matrices
        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,MAX_DEADLINE,methodName)
        matList=ulsGen.getAllPossibleMatrices()

        hList=[matList[0]]+[matList[1]]*MAX_DEADLINE
        mList=[matList[2]]+[matList[3]]*MAX_DEADLINE

        automaton=(MAX_DEADLINE,hList,mList)

        rec=RecRel(automaton,initialSet,T,nominalReachSet)
        stateList,dList,maxT=rec.getDeviations(p)

        print("\tMax Deviation: ",dList[maxT],";\t At time step: ",maxT)
        print("\tTotal Time Taken: ",time.time()-time_taken)
        print(">> End of Report!")
        #VizRS.vizDevs(dList,maxT)
        return (dList,maxT)

    def allPolicies():
        '''
        Initial Set: [[10,10],[10,10]]
        '''
        (dList_HK,maxT_HK)=FSMBased.holdAndKill() # 3 consecutive misses
        print("\n-----------\n")
        (dList_ZK,maxT_ZK)=FSMBased.zeroAndKill() # 3 consecutive misses
        print("\n-----------\n")
        (dList_HS,maxT_HS)=FSMBased.holdAndSkip() # 3 consecutive misses
        print("\n-----------\n")
        (dList_HSA,maxT_HSA)=FSMBased.holdAndSkipAny() # 3 consecutive misses
        print("\n-----------\n")

        labels=["HoldKill(3)","ZeroKill(3)","HoldSkip(3)","HoldSkipAny(3)"]
        allDevLists=[dList_HK,dList_ZK,dList_HS,dList_HSA]
        maxTLists=[maxT_HK,maxT_ZK,maxT_HS,maxT_HSA]

        VizRS.vizAllDevs(labels,allDevLists,maxTLists,"dc_motor_fsm")

    def compHoldSkipAny():
        (dList_HSA,maxT_HSA)=FSMBased.holdAndSkipAny(2) # 2 consecutive misses
        print("\n-----------\n")
        (dList_HSA_4,maxT_HSA_4)=FSMBased.holdAndSkipAny(4) # 4 consecutive misses
        print("\n-----------\n")
        (dList_HSA_8,maxT_HSA_8)=FSMBased.holdAndSkipAny(8) # 8 consecutive misses
        print("\n-----------\n")
        (dList_HSA_16,maxT_HSA_16)=FSMBased.holdAndSkipAny(16) # 8 consecutive misses
        print("\n-----------\n")

        labels=["HoldSkipAny(2)","HoldSkipAny(4)","HoldSkipAny(8)","HoldSkipAny(16)"]
        allDevLists=[dList_HSA,dList_HSA_4,dList_HSA_8,dList_HSA_16]
        maxTLists=[maxT_HSA,maxT_HSA_4,maxT_HSA_8,maxT_HSA_16]

        VizRS.vizAllDevs(labels,allDevLists,maxTLists,"dc_motor_hsa_comp_fsm")







if False:
    ULSBased.allPolicies()

if False:
    FSMBased.allPolicies()

if True:
    FSMBased.compHoldSkipAny()
