'''
Provides various benchmark examples
'''

import os,sys
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
import numpy as np
import scipy.linalg as LA
from scipy.integrate import quad

class Benchmarks:

    class DC2:
        '''
        DC Motor System example provided by Clara Hobbs.
        '''
        A=np.array(
        [[0.6065, 0.0373, 0.0021],
        [-0.007,0.9048, 0.0952],
        [0,0,0]]
        )
        B=np.array(
        [[0],
        [0],
        [1]]
        )
        C=np.array(
        [[1,0,0],
        [0,1,0]]
        )
        D=np.array(
        [[0],
        [0]]
        )
        K=np.array(
        [0.0020, 0.2482, 0.0261]
        )
        h=0.050
        d=0.050

    class DC:
        '''
        DC Motor System example provided by Clara Hobbs.
        '''
        A=np.array(
        [[0.5495, 0.0724],
        [0.0145,0.9332]
        ]
        )
        B=np.array(
        [[0.3781],
        [0.0523]
        ]
        )
        C=np.array(
        [[1,-1]
        ]
        )
        D=np.array(
        [[0]
        ]
        )
        Q=np.array(
        [[0.12, 0],
        [0,0.1]
        ]
        )
        R=np.array(
        [[0.05]
        ]
        )
        K=np.array(
        [
        [0.0977, 0.2504, 0.0781]
        ])
        K2=np.array(
        [
        [0.43616334, 0.48098159, 9999]
        ]
        )
        h=0.050
        d=0.050
        n=5 # Number of max deadline misses
