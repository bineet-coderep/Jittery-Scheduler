import os,sys
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
import copy
import numpy as np

class ULSGen:
    '''
    Computes the uncertain linear system, as per the benchmark
    and parameters
    '''

    def __init__(self,A,B,C,D,K,n):
        self.A=A # Dynamics
        self.B=B # Dynamics
        self.C=C # Dynamics
        self.D=D # Dynamics
        self.K=K # Control
        self.n=n # Maximum deadline misses allowed


    def getAllPossibleMatrices(self):
        '''
        Returns all possible matrices possible

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
        array_seqn.append(copy.copy(A_miss))

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
            array_seqn.append(A_hit[:,:,i])

        return array_seqn

    def getUncertainMatrix(self):
        '''
        Representation of an uncertain matrix:
            - A: nominal dynamics.
            - Er: a dictionary of errors:
                {
                    (i,j)=[a,b]
                }
                Uncertain Matrix[i][j] = A[i][j] + Er[(i,j)]

        Algo:
            - Obtain all possible matrices
            - Convert them to an Uncertain maytrix
        '''

        allMats=self.getAllPossibleMatrices()

        d=allMats[0].shape[0] # Dimension of the system

        A=np.zeros((d,d))
        Er={}

        for i in range(d):
            for j in range(d):
                # Find maximum and minimum value in (i,j) of all possible matrices
                max=-9999
                min=9999
                for m in allMats:
                    if m[i][j]>max:
                        max=m[i][j]
                    if m[i][j]<min:
                        min=m[i][j]
                if max==min:
                    A[i][j]=min
                else:
                    c=(max+min)/2
                    A[i][j]=c
                    Er[(i,j)]=[min-c,max-c]

        return (A,Er)
