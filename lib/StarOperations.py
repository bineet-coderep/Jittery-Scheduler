'''
Provides API to perform various operation on Star Sets
'''
import os,sys
import copy
import numpy as np
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
from Parameters import *
#import pypolycontain as pp


class StarOp:
    '''
    Implements various Star operations
    '''

    def prodMatStar(A,star):
        '''
        Returns the product of `A` with `star`
        '''
        C_list=star[0]
        C=np.array(C_list).reshape(-1,1)
        V=star[1]
        P=star[2]
        C_new_array=np.matmul(A,C)
        C_new=list(C_new_array.reshape(-1))
        V_new=np.matmul(A,V)
        P_new=copy.copy(P)

        return (C_new,V_new,P_new)

    @staticmethod
    def star2Zono(RS):
        C=RS[0]
        V=RS[1]
        P=RS[2]

        r=V.shape[0]
        c=V.shape[1]

        x=np.asarray(C).reshape(r,1)

        print(RS)

        G=np.zeros(V.shape)
        for i in range(r):
            for j in range(c):
                G[i][j]=V[i][j]*P[j][1]

        Z=pp.zonotope(x=x,G=G)

        print(x,G)

        return Z

    @staticmethod
    def zono2Star(Z):
        C=Z.x
        V=Z.G
        P=[(-1,1)]
        n=V.shape[0]
        c=V.shape[1]
        C=C.reshape(1,n)[0]
        P=P*c
        RS=(C,V,P)

        return RS
