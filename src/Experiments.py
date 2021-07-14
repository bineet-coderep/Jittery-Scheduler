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
        C=[0]*23
        V=np.zeros((23,23))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,12),(10,12)]
        P=P+[(1,1)]*21
        initialSet=(C,V,P)
        T=10

        treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,T)
        treeDict=treeObj.getTree()

        policyObj=Policy(treeDict,T)
        maxHeuSeqn=policyObj.getMaxTrajHeuristic()
        (z,maxHeuTraj)=policyObj.seqn2Traj(maxHeuSeqn,initialSet)
        #print(maxHeuSeqn)
        maxAlgoSeqn=policyObj.getOptMaxTraj()
        (z,maxAlgoTraj)=policyObj.seqn2Traj(maxAlgoSeqn,initialSet)
        #print(maxAlgoSeqn)
        #exit(0)
        trajs=[(maxHeuTraj,"Heuristic"),(maxAlgoTraj,"Optimal")]
        trajsComp=[]
        for j in range(20):
            (z,aRandTraj)=policyObj.getARandomTraj(initialSet)
            trajsComp.append(aRandTraj)
        VizRS.vizAllRS(trajs,trajsComp)




if True:
    Exp.test3()
