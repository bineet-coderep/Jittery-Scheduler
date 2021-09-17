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
from lib.ULSGenerator import *
from lib.Deviation import *
from lib.LQRSolver import *
from lib.BoundedTree import *

class Exp:

    def test1():
        # Using hold and skip

        C=[0]*13
        V=np.zeros((13,13))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(1,1)]*11
        initialSet=(C,V,P)
        T=150

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,Benchmarks.DC.n)
        #allMats=ulsGen.getAllPossibleMatrices()
        uncertainMat=ulsGen.getUncertainMatrix()
        print("Checkpoint1")
        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T)
        reachSets=deviation.getReachSets()
        print("Checkpoint2")
        VizRS.vizAllRS(reachSets[0])

    def test2():
        # Using zero and kill

        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(1,1)]*1
        initialSet=(C,V,P)
        T=150

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,Benchmarks.DC.n,"ZeroKill")
        #allMats=ulsGen.getAllPossibleMatrices()
        uncertainMat=ulsGen.getUncertainMatrix()
        print("Checkpoint1")
        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T)
        reachSets=deviation.getReachSets()
        print("Checkpoint2")
        VizRS.vizAllRS(reachSets[0])

    def test3():
        # Using hold and kill

        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(1,1)]*1
        initialSet=(C,V,P)
        T=150

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,Benchmarks.DC.n,"HoldKill")
        #allMats=ulsGen.getAllPossibleMatrices()
        uncertainMat=ulsGen.getUncertainMatrix()
        print("Checkpoint1")
        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T)
        reachSets=deviation.getReachSets()
        print("Checkpoint2")
        VizRS.vizAllRS(reachSets[0])

    def test4():
        lqrObj=LQR(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.Q,Benchmarks.DC.R)
        (K,X,e)=lqrObj.dlqr()
        print(K)

        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(1,1)]*1
        initialSet=(C,V,P)
        T=150

        ulsGen=ULSGen(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K2,Benchmarks.DC.n,"ZeroKill")
        #allMats=ulsGen.getAllPossibleMatrices()
        uncertainMat=ulsGen.getUncertainMatrix()
        print("Checkpoint1")
        deviation=Deviation(uncertainMat[0],uncertainMat[1],initialSet,T)
        reachSets=deviation.getReachSets()
        print("Checkpoint2")
        VizRS.vizAllRS(reachSets[0])

    def test5():
        # Using hold and skip

        C=[0]*3
        V=np.zeros((3,3))
        V[0][0]=1.0
        V[1][1]=1.0
        P=[(10,10),(10,10)]
        P=P+[(1,1)]*1
        initialSet=(C,V,P)
        T=150

        boundedTree=BoundedTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,T,initialSet,methodName="HoldKill")

        rsList=boundedTree.getBoundedTreeReachSets()

        VizRS.vizAllRS(rsList)

        print("Checkpoint2")








if True:
    Exp.test5()
