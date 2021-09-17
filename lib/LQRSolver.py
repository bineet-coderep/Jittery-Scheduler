import os,sys
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
import scipy
import numpy as np

class LQR:

    def __init__(self,A,B,Q,R):
        self.A=A
        self.B=B
        self.Q=Q
        self.R=R

    def dlqr(self):
        #first, try to solve the ricatti equation
        X = np.matrix(scipy.linalg.solve_discrete_are(self.A, self.B, self.Q, self.R))

        #compute the LQR gain
        K = np.matrix(scipy.linalg.inv(self.B.T*X*self.B+self.R)*(self.B.T*X*self.A))

        eigVals, eigVecs = scipy.linalg.eig(self.A-self.B*K)

        return K, X, eigVals
