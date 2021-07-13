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

    def test3():
        C=[0]*13
        V=np.array([
        [1,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        ])
        P=[(-1,1),(-1,1)]
        P=P+[(1,1)]*11
        initialSet=(C,V,P)
        T=5

        treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,T)
        treeDict=treeObj.getTree()

        policyObj=Policy(treeDict,T)
        maxHeuSeqn=policyObj.getMaxTrajHeuristic()
        (z,maxHeuTraj)=policyObj.seqn2Traj(maxHeuSeqn,initialSet)
        maxAlgoSeqn=policyObj.getOptMaxTraj()
        (z,maxAlgoTraj)=policyObj.seqn2Traj(maxAlgoSeqn,initialSet)
        trajs=[(maxHeuTraj,"Heuristic"),(maxAlgoTraj,"Optimal")]
        VizRS.vizAllRS(trajs,[])
        exit(0)
        allMissTraj=policyObj.getAllMissTraj()
        allHitTraj=policyObj.getAllHitTraj()
        trajsComp=[]
        for j in range(0):
            aRandTraj=policyObj.getARandomTraj()
            trajsComp.append((aRandTraj,""))
        trajsComp=trajsComp+[(allMissTraj,"All Miss"),(allHitTraj,"All Hit"),(maxHeuTraj,"SV Heu"),(maxAlgoTraj,"Optimal")]
        Viz.vizCompTraj(trajs,trajsComp)




if True:
    Exp.test3()
