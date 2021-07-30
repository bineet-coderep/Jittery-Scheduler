'''
This is to test various functionalities
'''

import os,sys
import random,numpy
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from lib.Benchmarks import *
from lib.Visualization import *
from lib.GenerateTree import *
from lib.Policies import *

class Exp:

    def test3():
        C=[0]*11
        V=np.zeros((11,11))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,12),(10,12)]
        P=P+[(1,1)]*9
        initialSet=(C,V,P)
        T=4

        projs=[0,1]

        treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,T)
        treeDict=treeObj.getTree()

        policyObj=Policy(treeDict,T)
        maxHeuSeqn=policyObj.getMaxTrajHeuristic(projs)
        (z,maxHeuTraj)=policyObj.seqn2Traj(maxHeuSeqn,initialSet)
        print(maxHeuSeqn)

        maxAlgoSeqn=policyObj.getOptMaxTraj(projs)
        (z,maxAlgoTraj)=policyObj.seqn2Traj(maxAlgoSeqn,initialSet)
        print(maxAlgoSeqn)

        #exit(0)
        (z,allMissTraj)=policyObj.getAllMissTraj(initialSet)
        (z,allHitTraj)=policyObj.getAllHitTraj(initialSet)
        (z,maxAlgoTraj)=policyObj.seqn2Traj(maxAlgoSeqn,initialSet)
        trajs=[(allHitTraj,"All Hit"),(allMissTraj,"All Miss"),(maxHeuTraj,"Heuristic"),(maxAlgoTraj,"Optimal")]
        trajsComp=[]
        for j in range(5):
            (z,aRandTraj)=policyObj.getARandomTraj(initialSet)
            trajsComp.append(aRandTraj)
        VizRS.vizAllRS(trajs,trajsComp)

    def test4():
        sZ=33
        C=[0]*sZ
        V=np.zeros((sZ,sZ))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,12),(10,12)]
        #P=[(20,22),(20,22)]
        P=P+[(1,1)]*(sZ-2)
        initialSet=(C,V,P)
        T=15

        projs=[0,1]
        projsX=[0]
        projsY=[1]

        treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,T)
        treeDict=treeObj.getTree()

        policyObj=Policy(treeDict,T)
        maxAlgoSeqn=policyObj.getOptMaxTraj(projs)
        (z,maxAlgoTraj)=policyObj.seqn2Traj(maxAlgoSeqn,initialSet)
        print("Optimal (X-Y): ",maxAlgoSeqn)

        policyObj=Policy(treeDict,T)
        maxAlgoSeqnVol=policyObj.getOptMaxTraj(projs,vol=True)
        (z,maxAlgoTrajVol)=policyObj.seqn2Traj(maxAlgoSeqnVol,initialSet)
        print("Optimal (XY Vol): ",maxAlgoSeqnVol)

        maxAlgoSeqnX=policyObj.getOptMaxTraj(projsX)
        (z,maxAlgoTrajX)=policyObj.seqn2Traj(maxAlgoSeqnX,initialSet)
        print("Optimal (X): ",maxAlgoSeqnX)

        maxAlgoSeqnY=policyObj.getOptMaxTraj(projsY)
        (z,maxAlgoTrajY)=policyObj.seqn2Traj(maxAlgoSeqnY,initialSet)
        print("Optimal (Y): ",maxAlgoSeqnY)

        (z,allMissTraj)=policyObj.getAllMissTraj(initialSet)

        (z,allHitTraj)=policyObj.getAllHitTraj(initialSet)

        trajs=[(allMissTraj,"All Miss"),(allHitTraj,"All Hit"),(maxAlgoTraj,"Optimal"),(maxAlgoTrajX,"Optimal (X)"),(maxAlgoTrajY,"Optimal (Y)"),(maxAlgoTrajVol,"Optimal (Vol)")]

        trajsComp=[]
        for j in range(20):
            (z,aRandTraj)=policyObj.getARandomTraj(initialSet)
            trajsComp.append(aRandTraj)
        VizRS.vizAllRS(trajs,trajsComp)




if True:
    Exp.test4()
