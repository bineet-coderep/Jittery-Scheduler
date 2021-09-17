import os,sys
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from lib.SetOperations import *
from lib.StarOperations import *
import math
import time

class BoundedTree:
    '''
    Implements Bounded Tree Based method
    '''
    def __init__(self,A,B,C,D,K,T,initSet,methodName="HoldSkip"):
        self.A=A # Dynamics
        self.B=B # Dynamics
        self.C=C # Dynamics
        self.D=D # Dynamics
        self.K=K # Control
        self.T=T # Max Time Step
        self.initialSet=initSet # Initial Set
        self.methodName=methodName # Scheduling policy

    def getOneStepReachSet(self,initSet):
        '''
        Get bounded time reachable set from one step
        '''
        # Generate all possible binary sequences
        seqLim=2**BOUNDED_TREE_STEP
        rsList=[]
        for s in range(seqLim):
            bin_t=[int(b) for b in list(format(s,'b'))]
            seqn=(BOUNDED_TREE_STEP-len(bin_t))*[0]+bin_t
            rsSeqn=self.getReachSetSeqn(initSet,seqn)
            rsList.append(copy.copy(rsSeqn))
        boxSet=SetOp.boxHull(rsList)
        return boxSet

    def getReachSetSeqn(self,initSet,seqn):
        '''
        Given a sequence, it returns the reachable set
        '''
        if self.methodName=="HoldSkip":
            return self.reachSetHoldSkip(initSet,seqn)
        elif self.methodName=="ZeroKill":
            return self.reachSetZeroKill(initSet,seqn)
        elif self.methodName=="HoldKill":
            return self.reachSetHoldKill(initSet,seqn)

    def reachSetHoldSkip(self,initSet,seqn):
        rs=copy.copy(initSet)
        p=self.A.shape[0]
        r=self.B.shape[1]
        n=BOUNDED_TREE_STEP

        # Miss matrix
        A_miss=np.vstack(
        (np.hstack((self.A,np.zeros((p,n*p)),self.B)),
        np.hstack((np.identity(n*p),np.zeros((n*p,p+r)))),
        np.hstack((np.zeros((r,(n+1)*p)),np.identity(r))))
        )

        # Hit matrix
        K_x = -self.K[:,0:p]
        if self.K.shape[1] == p + r:
            K_u = -self.K[:,p:p+r+1]
        else:
            K_u = np.zeros((p, r))

        A_hit=np.zeros(((n+1)*p + r, (n+1)*p + r, n+1))
        for i in range(n):
            A_hit[:,:,i]=np.vstack(
            (np.hstack((self.A,np.zeros((p,n*p)),self.B)),
            np.hstack((np.identity(n*p),np.zeros((n*p,p+r)))),
            np.hstack((np.zeros((r,i*p)),K_x,np.zeros((r,(n-i)*p)),K_u)))
            )

        # Get a sequence of arrays based on `seqn`
        #x_0=np.vstack((self.x0,np.zeros((p*n + r, 1))))
        t_max = len(seqn)
        t_since_last_hit = 0
        #x = np.zeros((p*(n+1) + r, t_max + 1));
        #x[:,0] = x_0[:,0];
        for t in range(1,t_max+1):
            if seqn[t-1]==1:
                # Hit
                A = A_hit[:,:,t_since_last_hit]
                t_since_last_hit = 0
            else:
                # Miss
                A = A_miss;
                t_since_last_hit = t_since_last_hit + 1
            rs=StarOp.prodMatStar(A,rs)

        #np.set_printoptions(precision=3)
        #print(x)
        #exit(0)
        return rs

    def reachSetHoldKill(self,initSet,seqn):
        rs=copy.copy(initSet)
        p=self.A.shape[0]
        r=self.B.shape[1]

        arrZ1=np.zeros((r,r))
        arrZ2=np.zeros((r,p))
        arrI=np.zeros((r,r))

        K_x = -self.K[:,0:p]
        A_hit=np.vstack((np.hstack((self.A,self.B)),np.hstack((K_x,arrZ1))))
        A_miss=np.vstack((np.hstack((self.A,self.B)),np.hstack((arrZ2,arrI))))

        t_max = len(seqn)

        for t in range(1,t_max+1):
            if seqn[t-1]==1:
                # Hit
                A = A_hit
            else:
                # Miss
                A = A_miss;
            rs=StarOp.prodMatStar(A,rs)

        #np.set_printoptions(precision=3)
        #print(x)
        #exit(0)
        return rs

    def reachSetZeroKill(self,initSet,seqn):
        rs=copy.copy(initSet)
        p=self.A.shape[0]
        r=self.B.shape[1]

        arrZ1=np.zeros((r,r))
        arrZ2=np.zeros((r,p))

        t_max = len(seqn)

        K_x = -self.K[:,0:p]
        A_hit=np.vstack((np.hstack((self.A,self.B)),np.hstack((K_x,arrZ1))))
        A_miss=np.vstack((np.hstack((self.A,self.B)),np.hstack((arrZ2,arrZ1))))

        for t in range(1,t_max+1):
            if seqn[t-1]==1:
                # Hit
                A = A_hit
            else:
                # Miss
                A = A_miss;
            rs=StarOp.prodMatStar(A,rs)

        #np.set_printoptions(precision=3)
        #print(x)
        #exit(0)
        return rs

    def getBoundedTreeReachSets(self):

        print(">> STATUS: Computing Bounded Step Reachable Sets . . .")
        time_taken=time.time()
        steps=math.ceil(self.T/BOUNDED_TREE_STEP)

        rs=copy.copy(self.initialSet)
        rsList=[copy.copy(rs)]

        for k in range(steps):
            print("\t>> SUBSTATUS: \tStep: ",k)
            rs=self.getOneStepReachSet(rs)
            rsList.append(copy.copy(rs))

        print("\t>> Time Taken: ",time.time()-time_taken)
        print(">> STATUS: Reachable Sets Computed!!")

        return rsList
