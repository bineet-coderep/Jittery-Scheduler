'''
Provides API to implement a policy --- a policy to find out maximum violation
'''
import os,sys
import numpy as np
import random
import time
import pickle
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
import scipy.linalg as LA
from lib.StarOperations import *


class Policy:
    '''
    APIs to implement various policies to find out the maximum violation
    '''

    def __init__(self,treeDict,T):
        self.treeDict=treeDict
        self.T=T

    def getAllMissTraj(self):
        '''
        Get the trajectory pertaining to all miss
        '''

        return []

    def getAllHitTraj(self):
        '''
        Get the trajectory pertaining to all miss
        '''

        return []

    def getARandomTraj(self):
        '''
        Get a random trajectory
        '''

        return []

    def seqn2Traj(self,seqn,initialSet):
        '''
        Given a seqn, returns the trajectory (and the sequence of arrys).
        Where, the initialSet is represented as a star: <C,V,P>
        '''

        ctNode=0
        arraySeqn=[]
        rs=initialSet
        trajs=[rs]
        for child in seqn:
            ctNode=self.treeDict[ctNode][1][child]
            arraySeqn.append(self.treeDict[ctNode][2])
            #print(self.treeDict[ctNode][2].shape,rs[0].shape)
            #np.set_printoptions(precision=1)
            #print(rs[1])
            #print("\n")
            rs=StarOp.prodMatStar(self.treeDict[ctNode][2],rs)
            trajs.append(rs)

        return (arraySeqn,trajs)

    def getMaxTrajHeuristic(self,pickleFlag=PICKLE_FLAG,picklePath=PICKLE_PATH):
        '''
        Implements the heuristic that chooses the path with max sigular value,
        at each step, from root to node
        '''
        ctNode=0
        seqn=[]

        print(">> STATUS: Applying Singular Value Based Heuristic . . .")
        time_taken=time.time()
        while ctNode!=-1:
            leftChild=self.treeDict[ctNode][1][0]
            rightChild=self.treeDict[ctNode][1][1]
            if leftChild==-1 or rightChild==-1:
                break;
            leftChildDyn=self.treeDict[leftChild][2]
            rightChildDyn=self.treeDict[rightChild][2]
            leftChildSV=LA.svdvals(leftChildDyn)[0]
            rightChildSV=LA.svdvals(rightChildDyn)[0]
            #print(leftChildSV,rightChildSV)
            if leftChildSV>rightChildSV:
                ctNode=leftChild
                seqn.append(0)
            else:
                ctNode=rightChild
                seqn.append(1)

        print("\t Time Taken: ",time.time()-time_taken)
        print(">> STATUS: Singular Value Heuristic Applied!\n")

        if pickleFlag==True:
            # Pickle the `seqm`
            with open(picklePath+'/'+'heuristic_trajectory_seqn.pickle', 'wb') as handle:
                pickle.dump(seqn, handle)


        return seqn

    def getOptMaxTraj(self,pickleFlag=PICKLE_FLAG,picklePath=PICKLE_PATH):
        '''
        Implements the DP like algorithm to find the maximum trajectory
        '''
        seqn=[]
        # Initialize V(.) and Pi(.)
        print(">> STATUS: Applying Singular Value Based Algorithm . . .")
        time_taken=time.time()
        V={}
        Pi={}
        for node in self.treeDict.keys():
            V[node]=self.treeDict[node][2]
            Pi[node]=node

        # Update V and Pi
        for i in range(self.T):
            for node in self.treeDict.keys():
                leftChild=self.treeDict[node][1][0]
                rightChild=self.treeDict[node][1][1]
                parentNode=self.treeDict[node][0]
                nodeDyn=self.treeDict[node][2]
                if leftChild!=-1 and rightChild!=-1:
                    leftChildDyn=self.treeDict[leftChild][2]
                    rightChildDyn=self.treeDict[rightChild][2]
                    V_new_left=np.matmul(nodeDyn,V[leftChild])
                    V_new_right=np.matmul(nodeDyn,V[rightChild])
                    V_new_left_SV=LA.svdvals(V_new_left)[0]
                    V_new_right_SV=LA.svdvals(V_new_right)[0]

                    if parentNode!=-1:
                        parentNodeDyn=self.treeDict[parentNode][2]
                        ABP_left=np.matmul(parentNodeDyn,V_new_left)
                        ABP_right=np.matmul(parentNodeDyn,V_new_right)
                        ABP_left_SVs=LA.svdvals(ABP_left)
                        ABP_right_SVs=LA.svdvals(ABP_right)

                    if V_new_left_SV>V_new_right_SV:
                        if parentNode>=0:
                            if ABP_left_SVs[0]<ABP_right_SVs[0]:
                                print("\t SUB-STATUS: Assumption Not Statisfied!","\tNode Number: ",node,"\tIt: ",i)
                        Pi[node]=leftChild
                        V[node]=V_new_left
                    else:
                        if parentNode>=0:
                            if ABP_right_SVs[-1]<ABP_left_SVs[0]:
                                print("\t SUB-STATUS: Assumption Not Statisfied!","\tNode Number: ",node,"\tIt: ",i)
                        Pi[node]=rightChild
                        V[node]=V_new_right


        print("\t Time Taken: ",time.time()-time_taken)
        print(">> STATUS: Singular Value Algorithm Applied!\n")
        seqn=self.Pi2Seq(Pi)

        if pickleFlag==True:
            # Pickle the `seqm`
            with open(picklePath+'/'+'optimal_trajectory_seqn.pickle', 'wb') as handle:
                pickle.dump(seqn, handle)

        return seqn

    def Pi2Seq(self,Pi):
        '''
        Given `Pi`, returns a `seqn` (0/1 vector) corresponding to
        `self.treeDict`
        '''
        ctNode=0
        seqn=[]

        while True:
            nextNode=Pi[ctNode]
            if ctNode==nextNode:
                break
            if self.treeDict[ctNode][1][0]==nextNode:
                seqn.append(0)
            else:
                seqn.append(1)
            ctNode=nextNode
        return seqn
