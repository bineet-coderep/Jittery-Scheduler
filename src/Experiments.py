'''
This is to test various functionalities
'''

import os,sys
import random
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from lib.Benchmarks import *
from lib.Visualization import *
from lib.GenerateTree import *
from lib.Policies import *

class Exp:

    def test0():
        x0=np.array([
        [1],
        [1]
        ])
        T=12

        treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,x0,T)
        (treeDict,trajs)=treeObj.getTree()

        policyObj=Policy(treeDict,trajs,T)
        allMissTraj=policyObj.getAllMissTraj()
        allHitTraj=policyObj.getAllHitTraj()
        aRandTraj=policyObj.getARandomTraj()

        trajsComp=[(allMissTraj,"All Miss"),(allHitTraj,"All Hit"),(aRandTraj,"Random")]
        Viz.vizCompTraj(trajs,trajsComp)


        # See some trajectories for N time steps
        T_large=25
        treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,x0,T_large)
        SAMP=50
        allHitSeqn=[1]*T_large
        (z,allHitTraj)=treeObj.getBranch(allHitSeqn)
        allMissSeqn=[0]*T_large
        (z,allMissTraj)=treeObj.getBranch(allMissSeqn)
        trajs=[allMissTraj]
        for i in range(SAMP):
            randSeqn=[random.randint(0,1) for t in range(T_large)]
            (z,aRandTraj)=treeObj.getBranch(randSeqn)
            trajs.append(aRandTraj)
        trajs.append(allHitTraj)
        Viz.vizAllTraj(trajs)


    def test1():
        x0=np.array([
        [1],
        [1]
        ])
        T=12

        treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,x0,T)
        (treeDict,trajs)=treeObj.getTree()

        policyObj=Policy(treeDict,trajs,T)
        maxHeuSeqn=policyObj.getMaxTrajHeuristic()
        (z,maxHeuTraj)=treeObj.getBranch(maxHeuSeqn)
        allMissTraj=policyObj.getAllMissTraj()
        allHitTraj=policyObj.getAllHitTraj()
        trajsComp=[]
        for j in range(100):
            aRandTraj=policyObj.getARandomTraj()
            trajsComp.append((aRandTraj,""))

        trajsComp=trajsComp+[(allMissTraj,"All Miss"),(allHitTraj,"All Hit"),(maxHeuTraj,"SV Heu")]
        Viz.vizCompTraj(trajs,trajsComp)


    def test2():
        x0=np.array([
        [1],
        [1]
        ])
        T=2

        treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,x0,T)
        (treeDict,trajs)=treeObj.getTree()

        policyObj=Policy(treeDict,trajs,T)
        maxHeuSeqn=policyObj.getMaxTrajHeuristic()
        (z,maxHeuTraj)=treeObj.getBranch(maxHeuSeqn)
        maxAlgoSeqn=policyObj.getOptMaxTraj()
        (z,maxAlgoTraj)=treeObj.getBranch(maxAlgoSeqn)
        allMissTraj=policyObj.getAllMissTraj()
        allHitTraj=policyObj.getAllHitTraj()
        trajsComp=[]
        for j in range(0):
            aRandTraj=policyObj.getARandomTraj()
            trajsComp.append((aRandTraj,""))
        trajsComp=trajsComp+[(allMissTraj,"All Miss"),(allHitTraj,"All Hit"),(maxHeuTraj,"SV Heu"),(maxAlgoTraj,"Optimal")]
        Viz.vizCompTraj(trajs,trajsComp)




if True:
    Exp.test1()
    Exp.test2()
