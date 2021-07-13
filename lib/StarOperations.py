'''
Provides API to perform various operation on Star Sets
'''
import os,sys
import copy
import numpy as np
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
from Parameters import *


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
