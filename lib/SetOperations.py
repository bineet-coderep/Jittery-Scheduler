import os,sys
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)
import copy
from Parameters import *
import numpy as np
import numpy.linalg as LA
from gurobipy import *
import math
import mpmath as mp

class SetOp:
    '''
    Computes the uncertain linear system, as per the benchmark
    and parameters
    '''

    def getDiamterOpt(rs):

        model = Model("qp")

        # Encode rs 1 . . .

        C1=copy.copy(rs[0])
        V1=copy.copy(rs[1])
        P1=copy.copy(rs[2])
        n1=len(C1)
        vecSize1=V1.shape[1]

        ## Encode predicate variables
        predVars1=[]
        for i in range(vecSize1):
            name="pred1_"+str(i)
            predVars1.append(model.addVar(-GRB.INFINITY,GRB.INFINITY,name=name,vtype='C'))
            model.addConstr(predVars1[i]>=P1[i][0],name+".1")
            model.addConstr(predVars1[i]<=P1[i][1],name+".2")

        ## Encode the states
        stateVars1=[]
        for i in range(n1):
            obj1=C1[i]
            for j in range(vecSize1):
                obj1=obj1+(V1[i][j]*predVars1[j])
            stateVars1.append(copy.copy(obj1))

        # . . . Encode rs 1 end



        # Encode rs 2 . . .

        C2=copy.copy(rs[0])
        V2=copy.copy(rs[1])
        P2=copy.copy(rs[2])
        n2=len(C2)
        vecSize2=V2.shape[1]

        ## Encode predicate variables
        predVars2=[]
        for i in range(vecSize2):
            name="pred2_"+str(i)
            predVars2.append(model.addVar(-GRB.INFINITY,GRB.INFINITY,name=name,vtype='C'))
            model.addConstr(predVars2[i]>=P2[i][0],name+".1")
            model.addConstr(predVars2[i]<=P2[i][1],name+".2")

        ## Encode the states
        stateVars2=[]
        for i in range(n2):
            obj2=C2[i]
            for j in range(vecSize2):
                obj2=obj2+(V2[i][j]*predVars2[j])
            stateVars2.append(copy.copy(obj2))

        # . . . Encode rs 2 end





        # Computing distance between the two

        dis=(stateVars1[3]-stateVars2[3])*(stateVars1[3]-stateVars2[3])

        # Set Objective
        model.setObjective(dis,GRB.MAXIMIZE) # Maximize the distance

        model.optimize()

        status = model.Status
        if status==GRB.Status.UNBOUNDED:
            print("UNBOUNDED ")
        else:
            if status == GRB.Status.INF_OR_UNBD or \
               status == GRB.Status.INFEASIBLE  or \
               status == GRB.Status.UNBOUNDED:
                print("INFEASIBLE")
            else:
                print('Obj: %g' % model.objVal)

    def getDiamter(rs):
        C=copy.copy(rs[0])
        V=copy.copy(rs[1])
        P=copy.copy(rs[2])
        sv=V.shape[0]
        aS=V.shape[1]


        #U=np.zeros((sv,1),dtype=object)

        dia=-9999

        for i in range(sv):
            s=0
            for j in range(aS):
                #print(P[j][0],P[j][1])
                s=s+(mp.mpi(P[j][0],P[j][1])*V[i][j])
            s=s+C[i]
            s_min=float(mp.nstr(s).split(',')[0][1:])
            s_max=float(mp.nstr(s).split(',')[1][:-1])
            d=abs(s_max-s_min)
            if d>dia:
                dia=d

        return dia

    def getSimpleRep(rsList):
        nominalRS=[]
        n=len(rsList[0][0])
        r=rsList[0][1].shape[1]
        for rs in rsList:
            P=rs[2]
            Vp=rs[1]
            Cp=rs[0]
            pt=[]
            for i in range(n):
                s=0
                s_min=0
                for j in range(r):
                    s=s+(mp.mpi(P[j][0],P[j][1])*Vp[i][j])
                s=s+Cp[i]
                s_min=float(mp.nstr(s).split(',')[0][1:])
                pt.append(s_min)
            nominalRS.append(pt)
        return nominalRS



    def boxHull(rsList):
        '''
        Given a set of reachable sets, compute a box-hull
        '''
        n=len(rsList[0][0])
        r=rsList[0][1].shape[1]

        U=np.zeros((n,1),dtype=object)

        for i in range(n):
            U[i][0]=(np.inf,-np.inf)

        for rs in rsList:
            P=rs[2]
            Vp=rs[1]
            Cp=rs[0]
            for i in range(n):
                s=0
                s_min=0
                s_max=0
                for j in range(r):
                    s=s+(mp.mpi(P[j][0],P[j][1])*Vp[i][j])
                s=s+Cp[i]
                s_min=float(mp.nstr(s).split(',')[0][1:])
                s_max=float(mp.nstr(s).split(',')[1][:-1])
                s_new_min=U[i][0][0]
                s_new_max=U[i][0][1]
                if s_min<U[i][0][0]:
                    s_new_min=s_min
                if s_max>U[i][0][1]:
                    s_new_max=s_max
                U[i][0]=(s_new_min,s_new_max)

        C_new=np.zeros(n)
        V_new=np.identity(n)
        P_new=[]

        for i in range(n):
            P_new.append((U[i][0][0],U[i][0][1]))

        box=(C_new,V_new,P_new)

        return box


    def getDistance2(st1,st2,p):
        '''
        Compute the distance between st1 and st2
        '''
        boxSt1=SetOp.boxHull([st1])[2][:p]
        boxSt2=SetOp.boxHull([st2])[2][:p]

        # Compute coordinates of boxSt1
        coordSt1=[]
        for element in itertools.product(*boxSt1):
            coordSt1.append(element)

        # Compute coordinates of boxSt2
        coordSt2=[]
        for element in itertools.product(*boxSt2):
            coordSt2.append(element)

        d=-np.inf

        print(coordSt1)

        '''for X1 in coordSt1:
            d_t=np.inf
            for X2 in coordSt2:
                t1=0
                for (x1,x2) in zip(X1,X2):
                    t1+=(x1-x2)**2
                d_l2=math.sqrt(t1)
                if d_l2<d_t:
                    d_t=d_l2
            if d_t>d:
                d=d_t'''

        '''for X1 in coordSt2:
            d_t=np.inf
            for X2 in coordSt1:
                t1=0
                for (x1,x2) in zip(X1,X2):
                    t1+=(x1-x2)**2
                d_l2=math.sqrt(t1)
                if d_l2<d_t:
                    d_t=d_l2
            if d_t>d:
                d=d_t
        '''

        return d

    def getDistance(st1,st2,p):
        '''
        Compute the distance between st1 and st2
        '''
        boxSt1=SetOp.boxHull([st1])[2][:p]
        boxSt2=SetOp.boxHull([st2])[2][:p]

        # Compute coordinates of boxSt1
        pt=[]
        for element in itertools.product(*boxSt1):
            pt.append(element)

        # Compute coordinates of boxSt2
        coordSt2=[]
        for element in itertools.product(*boxSt2):
            coordSt2.append(element)


        d=-np.inf
        for X1 in coordSt2:
            t1=0
            for (x1,x2) in zip(X1,pt[0]):
                t1+=(x1-x2)**2
            d_l2=math.sqrt(t1)
            if d_l2>d:
                d=d_l2



        return d





if False:
    C=[60,60]
    V=np.identity(2)
    P=[(10,12),(10,12)]
    SetOp.getDiamterInterval((C,V,P))
