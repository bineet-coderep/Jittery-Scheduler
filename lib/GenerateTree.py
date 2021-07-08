'''
Provides API to generate the scheduler tree
'''
import os,sys
import pickle
import time
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
import numpy as np
#from lib.Benchmarks import *
#from lib.Visualization import *

class GenTree:
    '''
    Generates a tree based on hit/miss of the scheduler.
    '''

    def __init__(self,A,B,C,D,K,x0,T):
        self.A=A # Dynamics Matrix A
        self.B=B # Dynamics Matrix B
        self.C=C # Dynamics Matrix C
        self.D=D # Dynamics Matrix D
        self.K=K # Feedback controller matrix
        self.x0=x0 # Initial Condition
        self.T=T # Max time for the simulation
        self.n=self.T # Maximum deadline misses allowed

    def getBranch(self,seqn):
        '''
        seqn: Boolean Vector.

        Given a `seqn` it returns a branch (as a list of arrays) in the tree, where the `seqn` of 0/1
        represents hit/miss

        This code has been taken from the Matlab implementation,
        `hold_and_skip_next.m`, by Clara Hobbs (also provided in this repository).
        '''

        p=self.A.shape[0]
        r=self.B.shape[1]

        array_seqn=[]


        # Miss matrix
        A_miss=np.vstack(
        (np.hstack((self.A,np.zeros((p,self.n*p)),self.B)),
        np.hstack((np.identity(self.n*p),np.zeros((self.n*p,p+r)))),
        np.hstack((np.zeros((r,(self.n+1)*p)),np.identity(r))))
        )

        # Hit matrix
        K_x = -self.K[:,0:p]
        if self.K.shape[1] == p + r:
            K_u = -self.K[:,p:p+r+1]
        else:
            K_u = np.zeros((p, r))

        A_hit=np.zeros(((self.n+1)*p + r, (self.n+1)*p + r, self.n+1))
        for i in range(self.n):
            A_hit[:,:,i]=np.vstack(
            (np.hstack((self.A,np.zeros((p,self.n*p)),self.B)),
            np.hstack((np.identity(self.n*p),np.zeros((self.n*p,p+r)))),
            np.hstack((np.zeros((r,i*p)),K_x,np.zeros((r,(self.n-i)*p)),K_u)))
            )

        # Get a sequence of arrays based on `seqn`
        x_0=np.vstack((self.x0,np.zeros((p*self.n + r, 1))))
        t_max = len(seqn)
        t_since_last_hit = 0
        x = np.zeros((p*(self.n+1) + r, t_max + 1));
        x[:,0] = x_0[:,0];
        for t in range(1,t_max+1):
            if seqn[t-1]==1:
                # Hit
                A = A_hit[:,:,t_since_last_hit]
                t_since_last_hit = 0
            else:
                # Miss
                A = A_miss;
                t_since_last_hit = t_since_last_hit + 1
            array_seqn.append(A)
            x[:,t] = np.matmul(A, x[:,t-1])

        return (array_seqn,x)

    def getTree(self,pickleFlag=PICKLE_FLAG,picklePath=PICKLE_PATH):
        '''
        Returns the tree and trajectories
        '''

        # Generate all possible binary sequences
        print(">> STATUS: Generating Tree . . .")
        time_taken=time.time()
        seqLim=2**self.T
        treeList=[]
        trajs=[]
        for s in range(seqLim):
            bin_t=[int(b) for b in list(format(s,'b'))]
            seqn=(self.T-len(bin_t))*[0]+bin_t
            #print(seqn)
            (array_seqn,traj)=self.getBranch(seqn)
            treeList.append((seqn,array_seqn))
            trajs.append(traj)

        #Viz.vizAllTraj(trajs)

        treeDict=GenTree.dictionaryFy(treeList)

        if pickleFlag==True:
            # Pickle the `treeDict`
            with open(picklePath+'/'+'tree.pickle', 'wb') as handle:
                pickle.dump(treeDict, handle)

            # Pickle the `trajs`
            with open(picklePath+'/'+'all_trajectories.pickle', 'wb') as handle:
                pickle.dump(trajs, handle)


        print("\t Time Taken: ",time.time()-time_taken)

        print(">> STATUS: Tree Generated!\n")

        return (treeDict,trajs)

    def dictionaryFy(treeList):
        '''
        Given a treeList, populate and save `treeDict`

        treeList=[(seqnOfMissHit, dynamicsMatrixOfTheSeqn)]

        treeDict:
        {
            nodeNumber: [parentNodeNumber, [leftChild, rightChild], dynamicsMatrix]
        }
        '''

        treeDict={} # Dictionary to store the tree

        treeDict[0]=[-1,[-1,-1],np.identity(2)] # 0 is the root of the tree

        treeNodeNumber=1 # Numbering the nodes of the tree

        for (seqn,array_seqn) in treeList:
            ctNode=0 # Current node
            for i in range(len(seqn)):

                # Check if seqn[i]-child is available
                if treeDict[ctNode][1][seqn[i]]==-1:
                    # Unavailable
                    # Create a Node for seqn[i]
                    treeDict[treeNodeNumber]=[ctNode,[-1,-1],array_seqn[i]]
                    treeDict[ctNode][1][seqn[i]]=treeNodeNumber
                    ctNode=treeNodeNumber
                    treeNodeNumber=treeNodeNumber+1
                else:
                    # Available
                    ctNode=treeDict[ctNode][1][seqn[i]]

        treeDict[0][2]=np.identity(treeDict[1][2].shape[0])

        if False:
            for key in treeDict:
                print(key,": \t\t","P: ",treeDict[key][0],"\tC: \t",treeDict[key][1])



        return treeDict









if False:
    x0=np.array([
    [1],
    [1]
    ])
    treeObj=GenTree(Benchmarks.DC.A,Benchmarks.DC.B,Benchmarks.DC.C,Benchmarks.DC.D,Benchmarks.DC.K,x0,12)
    treeObj.getTree()
