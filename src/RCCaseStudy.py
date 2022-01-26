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

    def holdAndKill(P=[(10,10),(10,10)],T=150):
        '''
        - Applies Hold&Kill scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - All possible sequences of hit/miss
        '''
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
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

        VizRS.vizAllRSPng(reachORS,nominalReachSet,policyname="Zero&Kill",fname="rc_uls_hk")

        return (dList,maxT)

    def zeroAndKill(P=[(10,10),(10,10)],T=150):
        '''
        - Applies Zero&Kill scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - All possible sequences of hit/miss
        '''
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
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
        #print(len(reachORS),len(nominalReachSet))
        VizRS.vizAllRSPng(reachORS,nominalReachSet,policyname="Zero&Kill",fname="rc_uls_zk")

        return (dList,maxT)

    def holdAndSkip(P=[(10,10),(10,10)],T=150):
        '''
        - Applies Hold&Skip scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - 3 consecutive misses allowed
        '''
        C_nom=[0]*3
        V_nom=np.zeros((3,3))
        V_nom[0][0]=1.0
        V_nom[1][1]=1.0
        P_nom=P
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

    def holdAndSkipAny(P=[(10,10),(10,10)],T=150):
        '''
        - Applies Hold&Skip scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - All possible sequences of hit/miss
        '''

        C=[0]*5
        V=np.zeros((5,5))
        V[0][0]=1.0
        V[1][1]=1.0
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

    def zeroAndSkipNext(P=[(10,10),(10,10)],T=150):
        '''
        - Applies Hold&Skip scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - All possible sequences of hit/miss
        '''

        C=[0]*5
        V=np.zeros((5,5))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*5
        initialSet=(C,V,P)
        T=150
        nominalSeqn=[1]*T
        MAX_DEADLINE=-1 # Any
        methodName="ZeroSkipNext"
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

    def allPolicies(P=[(10,10),(10,10)],T=150):
        '''
        Initial Set: [[10,10],[10,10]]
        '''
        (dList_HK,maxT_HK)=ULSBased.holdAndKill(P,T) # Any number of miss
        print("\n-----------\n")
        (dList_ZK,maxT_ZK)=ULSBased.zeroAndKill(P,T) # Any number of miss
        print("\n-----------\n")
        #(dList_HS,maxT_HS)=ULSBased.holdAndSkip(P,T) # 3 consecutive misses
        #print("\n-----------\n")
        (dList_HSA,maxT_HSA)=ULSBased.holdAndSkipAny(P,T) # Any number of miss
        print("\n-----------\n")
        (dList_ZSN,maxT_ZSN)=ULSBased.zeroAndSkipNext(P,T) # Any number of miss
        print("\n-----------\n")

        labels=["ZeroKill"]
        allDevLists=[dList_ZK]
        maxTLists=[maxT_ZK]

        VizRS.vizAllDevs(labels,allDevLists,maxTLists,"rc_uls")


class FSMBased:

    def holdAndKill(P=[(10,10),(10,10)],MAX_DEADLINE=3,T=150):
        '''
        - Applies Hold&Kill scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        nominalSeqn=[1]*T
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
        VizRS.vizAllNMissesFSM(stateList,nominalReachSet,policyname="Hold&Kill",fname="rc_fsm_hk")
        return (dList,maxT)

    def zeroAndKill(P=[(10,10),(10,10)],MAX_DEADLINE=3,T=150):
        '''
        - Applies Zero&Kill scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        nominalSeqn=[1]*T
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
        VizRS.vizAllNMissesFSM(stateList,nominalReachSet,policyname="Zero&Kill",fname="rc_fsm_zk")
        return (dList,maxT)

    def holdAndSkip(P=[(10,10),(10,10)],MAX_DEADLINE=3,T=150):
        '''
        - Applies Hold&Skip scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''
        C_nom=[0]*3
        V_nom=np.zeros((3,3))
        V_nom[0][0]=1.0
        V_nom[1][1]=1.0
        P_nom=P
        P_nom=P_nom+[(0,0)]*1
        initialSet_nom=(C_nom,V_nom,P_nom)

        C=[0]*9
        V=np.zeros((9,9))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*7
        initialSet=(C,V,P)
        nominalSeqn=[1]*T
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

    def holdAndSkipAny(P=[(10,10),(10,10)],MAX_DEADLINE=3,T=150):
        '''
        - Applies Hold&SkipAny scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''

        C=[0]*5
        V=np.zeros((5,5))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*3
        initialSet=(C,V,P)
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
        VizRS.vizAllNMissesFSM(stateList,nominalReachSet,policyname="Hold&Skip-Next",fname="rc_fsm_hs")
        return (dList,maxT)

    def zeroAndSkipNext(P=[(10,10),(10,10)],MAX_DEADLINE=3,T=150):
        '''
        - Applies Hold&SkipAny scheduling policy
        - Returns the maximum deviation from the nominal behavior
        - N consecutive misses allowed
        '''

        C=[0]*5
        V=np.zeros((5,5))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*3
        initialSet=(C,V,P)
        nominalSeqn=[1]*T
        methodName="ZeroSkipNext"
        p=Benchmarks.DC.A.shape[0]

        print(">> REPORT.\tMethod: Recurrence Relation.\tPolicy: ",methodName,".\tMax Deadline Miss: ",MAX_DEADLINE)
        time_taken=time.time()

        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetZeroSkipNext(initialSet,nominalSeqn)

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
        VizRS.vizAllNMissesFSM(stateList,nominalReachSet,policyname="Zero&Skip-Next",fname="rc_fsm_zs")
        return (dList,maxT)

    def allPolicies(P=[(10,10),(10,10)],MAX_DEADLINE=3,T=150):
        '''
        Initial Set: [[10,10],[10,10]]
        '''
        (dList_HK,maxT_HK)=FSMBased.holdAndKill(P,MAX_DEADLINE,T)
        print("\n-----------\n")
        (dList_ZK,maxT_ZK)=FSMBased.zeroAndKill(P,MAX_DEADLINE,T)
        print("\n-----------\n")
        #(dList_HS,maxT_HS)=FSMBased.holdAndSkip()
        #print("\n-----------\n")
        (dList_HSA,maxT_HSA)=FSMBased.holdAndSkipAny(P,MAX_DEADLINE,T)
        print("\n-----------\n")
        (dList_ZSN,maxT_ZSN)=FSMBased.zeroAndSkipNext(P,MAX_DEADLINE,T)
        print("\n-----------\n")

        labels=["Hold&Kill("+str(MAX_DEADLINE)+")","Zero&Kill("+str(MAX_DEADLINE)+")","Hold&Skip-Next("+str(MAX_DEADLINE)+")","Zero&Skip-Next("+str(MAX_DEADLINE)+")"]
        allDevLists=[dList_HK,dList_ZK,dList_HSA,dList_ZSN]
        maxTLists=[maxT_HK,maxT_ZK,maxT_HSA,maxT_ZSN]

        VizRS.vizAllDevs(labels,allDevLists,maxTLists,"rc_fsm")

    def compHoldSkipAny(P=[(10,10),(10,10)],missList=[2,4,8,16],T=150):

        labels=[]
        allDevLists=[]
        maxTLists=[]
        for m in missList:

            (dList_HSA,maxT_HSA)=FSMBased.holdAndSkipAny(P,m,T)
            print("\n-----------\n")
            labels.append("Hold&Skip-Next("+str(m)+")")
            allDevLists.append(dList_HSA)
            maxTLists.append(maxT_HSA)

        VizRS.vizAllDevs(labels,allDevLists,maxTLists,"rc_hsa_comp_fsm")

    def compHoldSkipAnyInitSet(PList=[[(10,10),(10,10)],[(-10,-10),(-10,-10)]],MAX_DEADLINE=3,T=150):

        labels=[]
        allDevLists=[]
        maxTLists=[]
        for P in PList:

            (dList_HSA,maxT_HSA)=FSMBased.holdAndSkipAny(P,MAX_DEADLINE,T)
            print("Init Set: ",P[0][0],",",P[1][0])
            print("\n-----------\n")
            labels.append("Hold&Skip-Next ("+str(P[0][0])+","+str(P[1][0])+")")
            allDevLists.append(dList_HSA)
            maxTLists.append(maxT_HSA)

        VizRS.vizAllDevs(labels,allDevLists,maxTLists,"rc_hsa_comp_init_fsm")


class CompStability:

    def isSafe(P=[(10,10),(10,10)],T=150,methodName="ZeroKill",maxDeadline=3,safeDev=1.92):
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        nominalSeqn=[1]*T
        p=Benchmarks.DC.A.shape[0]


        nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldKill(initialSet,nominalSeqn)
        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,maxDeadline,methodName)

        # Using ULS method
        time_taken_uls=time.time()
        uncertainMat=ulsGen.getUncertainMatrix()
        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T,nominalReachSet)
        (reachORS,dList_ULS,maxT_ULS)=deviation.getDeviations(p)
        time_taken_uls=time.time()-time_taken_uls

        # Using FSM Based
        time_taken_fsm=time.time()
        matList=ulsGen.getAllPossibleMatrices()
        hList=[matList[0]]*(maxDeadline+1)
        mList=[matList[1]]*maxDeadline
        automaton=(maxDeadline,hList,mList)
        rec=RecRel(automaton,initialSet,T,nominalReachSet)
        stateList,dList_FSM,maxT_FSM=rec.getDeviations(p)
        time_taken_fsm=time.time()-time_taken_fsm

        # Report
        print("\tULS time taken: ",time_taken_uls,"; \tFSM time taken: ",time_taken_fsm)
        print("\tULS max dev: ",dList_ULS[maxT_ULS],"; \tFSM time taken: ",dList_FSM[maxT_FSM])

        # Plot the safety envelopes
        Viz.plotSafetyEnv(nominalReachSet,dList_ULS,maxT_ULS,safeDev,fname="rc-uls-"+methodName)
        Viz.plotSafetyEnv(nominalReachSet,dList_FSM,maxT_FSM,safeDev,fname="rc-fsm-"+methodName)

class CompScalability:

    def timeH(P=[(10,10),(10,10)],timeSteps=[50,300,50],methodName="ZeroKill",maxDeadline=3):
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        p=Benchmarks.DC.A.shape[0]

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,maxDeadline,methodName)

        # Using ULS method
        timeList_ULS=[]
        maxDevList_ULS=[]
        labels_ULS=[]
        uncertainMat=ulsGen.getUncertainMatrix()
        for T in range(timeSteps[0],timeSteps[1],timeSteps[2]):
            time_taken_uls=time.time()
            nominalSeqn=[1]*T
            nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldKill(initialSet,nominalSeqn)
            deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T,nominalReachSet)
            (reachORS,dList_ULS,maxT_ULS)=deviation.getDeviations(p)
            time_taken_uls=time.time()-time_taken_uls
            timeList_ULS.append(time_taken_uls)
            maxDevList_ULS.append(dList_ULS[maxT_ULS])
            labels_ULS.append(str("{:.2f}".format(dList_ULS[maxT_ULS]))+","+str(T))


        Viz.plotScalability(timeList_ULS,maxDevList_ULS,labels_ULS)

        # Using FSM Based
        timeList_FSM=[]
        maxDevList_FSM=[]
        labels_FSM=[]
        matList=ulsGen.getAllPossibleMatrices()
        hList=[matList[0]]*(maxDeadline+1)
        mList=[matList[1]]*maxDeadline
        automaton=(maxDeadline,hList,mList)
        for T in range(timeSteps[0],timeSteps[1],timeSteps[2]):
            time_taken_fsm=time.time()
            nominalSeqn=[1]*T
            nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldKill(initialSet,nominalSeqn)
            rec=RecRel(automaton,initialSet,T,nominalReachSet)
            stateList,dList_FSM,maxT_FSM=rec.getDeviations(p)
            time_taken_fsm=time.time()-time_taken_fsm
            timeList_FSM.append(time_taken_fsm)
            maxDevList_FSM.append(dList_FSM[maxT_FSM])
            labels_FSM.append(str("{:.2f}".format(dList_FSM[maxT_FSM]))+", "+str(T))


        Viz.plotScalability(timeList_FSM,maxDevList_FSM,labels_FSM)

    def maxDeadlineVary(P=[(10,10),(10,10)],deadlines=[1,6,1],methodName="ZeroKill",T=150):
        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=P+[(0,0)]*1
        initialSet=(C,V,P)
        p=Benchmarks.DC.A.shape[0]

        # Using ULS method
        timeList_ULS=[]
        maxDevList_ULS=[]
        labels_ULS=[]
        for maxDeadline in range(deadlines[0],deadlines[1],deadlines[2]):
            time_taken_uls=time.time()
            ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,maxDeadline,methodName)
            uncertainMat=ulsGen.getUncertainMatrix()
            nominalSeqn=[1]*T
            nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldKill(initialSet,nominalSeqn)
            deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T,nominalReachSet)
            (reachORS,dList_ULS,maxT_ULS)=deviation.getDeviations(p)
            time_taken_uls=time.time()-time_taken_uls
            timeList_ULS.append(time_taken_uls)
            maxDevList_ULS.append(dList_ULS[maxT_ULS])
            labels_ULS.append(str("{:.2f}".format(dList_ULS[maxT_ULS]))+","+str(maxDeadline))


        Viz.plotScalability(timeList_ULS,maxDevList_ULS,labels_ULS)

        # Using FSM Based
        timeList_FSM=[]
        maxDevList_FSM=[]
        labels_FSM=[]
        for maxDeadline in range(deadlines[0],deadlines[1],deadlines[2]):
            time_taken_fsm=time.time()
            ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,maxDeadline,methodName)
            matList=ulsGen.getAllPossibleMatrices()
            hList=[matList[0]]*(maxDeadline+1)
            mList=[matList[1]]*maxDeadline
            automaton=(maxDeadline,hList,mList)
            nominalSeqn=[1]*T
            nominalReachSet=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K).reachSetHoldKill(initialSet,nominalSeqn)
            rec=RecRel(automaton,initialSet,T,nominalReachSet)
            stateList,dList_FSM,maxT_FSM=rec.getDeviations(p)
            time_taken_fsm=time.time()-time_taken_fsm
            timeList_FSM.append(time_taken_fsm)
            maxDevList_FSM.append(dList_FSM[maxT_FSM])
            labels_FSM.append(str("{:.2f}".format(dList_FSM[maxT_FSM]))+", "+str(maxDeadline))


        Viz.plotScalability(timeList_FSM,maxDevList_FSM,labels_FSM)






if False:
    CompStability.isSafe()

if True:
    CompScalability.timeH()
    CompScalability.maxDeadlineVary()
