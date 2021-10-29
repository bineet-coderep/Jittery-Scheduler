'''
Provides API to visualize various artifacts
'''

import os,sys
import random
import matplotlib.pyplot as plt
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from gurobipy import *
import time
import os
import imageio
from lib.StarOperations import *
#import pypolycontain as pp


class VizRS:

    def getPlotsLineFine(star,theta1,theta2):
        '''
        Returns the list of points (x,y)
        for the reachable set st1
        '''

        C=star[0]
        V=star[1]
        P=star[2]
        X_list=[]
        Y_list=[]

        sv=V.shape[0]
        aS=V.shape[1]

        semiDefFlag=False
        model = Model("qp")
        model.setParam( 'OutputFlag', False )

        # Create Predicate Variables
        predVars=[]
        for i in range(aS):
            name="Pred"+str(i)
            predVars.append(model.addVar(-GRB.INFINITY,GRB.INFINITY,name=name,vtype='C'))
        #-----------------------

        # Axes Variables
        X=model.addVar(-GRB.INFINITY,GRB.INFINITY,name="X",vtype='C')
        Y=model.addVar(-GRB.INFINITY,GRB.INFINITY,name="Y",vtype='C')
        #-------------------------

        # Create the Star Constraints
        objX=0
        for i in range(aS):
            objX=objX+(predVars[i]*V[theta1][i])
        objX=C[theta1]+objX

        objY=0
        for i in range(aS):
            objY=objY+(predVars[i]*V[theta2][i])
        objY=C[theta2]+objY

        model.addConstr(X==objX,"X Axis")
        model.addConstr(Y==objY,"Y Axis")
        #-----------------------------------

        # Predicate Constraints
        for i in range(aS):
            a=P[i][0]
            b=P[i][1]
            if a==b:
                model.addConstr(predVars[i]==a,name)
            else:
                model.addConstr(predVars[i]>=min(a,b),name+".1")
                model.addConstr(predVars[i]<=max(a,b),name+".2")
        #-----------------------------------


        # Quadrant Specific Constraints

        # 1st Quadrant

        obj=X+Y
        model.setObjective(obj,GRB.MAXIMIZE)

        C_x=0
        C_y=0
        for a in range(900):
            an=a/10
            if an==90:
                model.addConstr(X==0+C_x,"Angle")
            else:
                m=math.tan(math.radians(an))
                model.addConstr(Y==m*(X)+C_y,"Angle")
            try:
                model.optimize()
                #model.write("dump.bas")
                status = model.Status
                if status==GRB.Status.UNBOUNDED:
                    print("UNBOUNDED ")
                else:
                    if status == GRB.Status.INF_OR_UNBD or \
                       status == GRB.Status.INFEASIBLE  or \
                       status == GRB.Status.UNBOUNDED:
                        0;
                        #print('**The model cannot be solved because it is infeasible or unbounded**')
                    else:
                        xVal=model.getVarByName("X").x
                        yVal=model.getVarByName("Y").x
                        X_list.append(xVal)
                        Y_list.append(yVal)
            except:
                semiDefFlag=True

            if semiDefFlag==True:
                print("Shoot!!")

            semiDefFlag=False
            model.remove(model.getConstrByName("Angle"))
        #-----------------------------

        #'''
        # 2nd Quadrant

        obj=X-Y
        model.setObjective(obj,GRB.MAXIMIZE)

        for a in range(0,-900,-1):
            an=a/10
            if an==-90:
                model.addConstr(X==0,"Angle")
            else:
                m=math.tan(math.radians(an))
                model.addConstr(Y==m*X,"Angle")
            try:
                model.optimize()
                #model.write("dump.bas")
                status = model.Status
                if status==GRB.Status.UNBOUNDED:
                    print("UNBOUNDED ")
                else:
                    if status == GRB.Status.INF_OR_UNBD or \
                       status == GRB.Status.INFEASIBLE  or \
                       status == GRB.Status.UNBOUNDED:
                        0;
                        #print('**The model cannot be solved because it is infeasible or unbounded**')
                    else:
                        xVal=model.getVarByName("X").x
                        yVal=model.getVarByName("Y").x
                        X_list.append(xVal)
                        Y_list.append(yVal)
            except:
                semiDefFlag=True

            if semiDefFlag==True:
                print("Shoot!!")

            semiDefFlag=False
            model.remove(model.getConstrByName("Angle"))
        #-----------------------------

        # 3rd Quadrant

        obj=-X-Y
        model.setObjective(obj,GRB.MAXIMIZE)

        for a in range(-900,-1800,-1):
            an=a/10
            if an==-90:
                model.addConstr(X==0,"Angle")
            else:
                m=math.tan(math.radians(an))
                model.addConstr(Y==m*X,"Angle")
            try:
                model.optimize()
                #model.write("dump.bas")
                status = model.Status
                if status==GRB.Status.UNBOUNDED:
                    print("UNBOUNDED ")
                else:
                    if status == GRB.Status.INF_OR_UNBD or \
                       status == GRB.Status.INFEASIBLE  or \
                       status == GRB.Status.UNBOUNDED:
                        0;
                        #print('**The model cannot be solved because it is infeasible or unbounded**')
                    else:
                        xVal=model.getVarByName("X").x
                        yVal=model.getVarByName("Y").x
                        X_list.append(xVal)
                        Y_list.append(yVal)
            except:
                semiDefFlag=True

            if semiDefFlag==True:
                print("Shoot!!")

            semiDefFlag=False
            model.remove(model.getConstrByName("Angle"))
        #-----------------------------

        # 4th Quadrant

        obj=-X+Y
        model.setObjective(obj,GRB.MAXIMIZE)

        for a in range(900,1800):
            an=a/10
            if an==90:
                model.addConstr(X==0,"Angle")
            else:
                m=math.tan(math.radians(an))
                model.addConstr(Y==m*X,"Angle")
            try:
                model.optimize()
                #model.write("dump.bas")
                status = model.Status
                if status==GRB.Status.UNBOUNDED:
                    print("UNBOUNDED ")
                else:
                    if status == GRB.Status.INF_OR_UNBD or \
                       status == GRB.Status.INFEASIBLE  or \
                       status == GRB.Status.UNBOUNDED:
                        0;
                        #print('**The model cannot be solved because it is infeasible or unbounded**')
                    else:
                        xVal=model.getVarByName("X").x
                        yVal=model.getVarByName("Y").x
                        X_list.append(xVal)
                        Y_list.append(yVal)
            except:
                semiDefFlag=True

            if semiDefFlag==True:
                print("Shoot!!")

            semiDefFlag=False
            model.remove(model.getConstrByName("Angle"))
        #-----------------------------



        #------------------------------

        #print(X_list,Y_list)
        #exit(0)
        #'''

        return (X_list,Y_list)

    def vizAllRS(trajs,nomTrajs,th1=0,th2=1,fname="all_trajectories"):

        print(">> STATUS: Visualizing Reachable Sets . . .")
        time_taken=time.time()

        plt.figure()

        ct=0
        fnames=[]
        for (rs,nom) in zip(trajs,nomTrajs):
            #print(rs)
            if ct%math.floor(100/VIZ_PER_COVERAGE)==0:
                (X,Y)=VizRS.getPlotsLineFine(rs,th1,th2)
                plt.scatter(X,Y,s=2)
                (X_nom,Y_nom)=VizRS.getPlotsLineFine(nom,th1,th2)
                print(X_nom,Y_nom)
                plt.scatter(X_nom,Y_nom,s=2,c="k")
                fnameTmp=OUTPUT_PATH+'/'+fname+str(ct)+".png"
                fnames.append(fnameTmp)
                plt.savefig(fnameTmp)
            ct=ct+1
            #plt.close()

        with imageio.get_writer(OUTPUT_PATH+'/'+fname+'gif.gif', mode='I',fps=2) as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)

        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Reachable Sets Visualized!")

    def vizDevs(devList,maxT):
        T=len(devList)
        X=list(range(T))
        plt.figure()
        plt.plot(X,devList)
        plt.scatter(maxT,devList[maxT],s=50,c='red')
        plt.show()

    def vizAllDevs(labels,devLists,maxTLists,fname="benchmark"):

        T=len(devLists[0])
        X=list(range(T))
        plt.figure()
        plt.xlabel("Deviation",fontsize=20)
        plt.ylabel("Time",fontsize=20)

        for (lb,devList,maxT) in zip(labels,devLists,maxTLists):
            plt.plot(X,devList,label=lb)
            plt.scatter(maxT,devList[maxT],s=100)
            plt.text(maxT+0.1,devList[maxT],str(maxT)+","+"{:.2f}".format(devList[maxT]),fontsize='x-large')

        plt.legend(fontsize='x-large')
        plt.savefig(OUTPUT_PATH+'/'+fname+"_all_devs")



    def vizAllRS2(trajs,th1=0,th2=1,fname="all_trajectories"):

        print(">> STATUS: Visualizing Reachable Sets . . .")
        time_taken=time.time()

        plt.figure()

        ct=0
        fnames=[]
        for rs in trajs:
            #print(rs)
            if ct%math.floor(100/VIZ_PER_COVERAGE)==0:
                (X,Y)=VizRS.getPlotsLineFine(rs,th1,th2)
                plt.scatter(X,Y,s=2)
                fnameTmp=OUTPUT_PATH+'/'+fname+str(ct)+".png"
                fnames.append(fnameTmp)
                plt.savefig(fnameTmp)
            ct=ct+1
            #plt.close()

        with imageio.get_writer(OUTPUT_PATH+'/'+fname+'gif.gif', mode='I',fps=2) as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)

        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Reachable Sets Visualized!")

    def vizAllTwoMissesFSM(S0,S1,S2,th1=0,th2=1,fname="fsm_all_trajectories"):

        print(">> STATUS: Visualizing Reachable Sets . . .")
        time_taken=time.time()

        plt.figure()

        ct=0
        fnames=[]
        for (s0,s1,s2) in zip(S0,S1,S2):
            #print(rs)
            if ct%math.floor(100/VIZ_PER_COVERAGE)==0:
                # Visualize S0
                (X,Y)=VizRS.getPlotsLineFine(s0,th1,th2)
                plt.scatter(X,Y,s=2)
                # Visualize S1
                if s1!=-1:
                    (X1,Y1)=VizRS.getPlotsLineFine(s1,th1,th2)
                    plt.scatter(X1,Y1,s=2)
                # Visualize S2
                if s2!=-1:
                    (X2,Y2)=VizRS.getPlotsLineFine(s2,th1,th2)
                    plt.scatter(X2,Y2,s=2)
                fnameTmp=OUTPUT_PATH+'/'+fname+str(ct)+".png"
                fnames.append(fnameTmp)
                plt.savefig(fnameTmp)
            ct=ct+1
            #plt.close()

        with imageio.get_writer(OUTPUT_PATH+'/'+fname+'gif.gif', mode='I',fps=2) as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)

        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Reachable Sets Visualized!")

    def vizAllNMissesFSM(statesList,th1=0,th2=1,fname="fsm_all_trajectories"):

        print(">> STATUS: Visualizing Reachable Sets . . .")
        time_taken=time.time()
        nStates=len(statesList)
        T=len(statesList[0])

        plt.figure()

        ct=0
        fnames=[]
        for t in range(T):
            #print(rs)
            if ct%math.floor(100/VIZ_PER_COVERAGE)==0:

                for i in range(nStates):
                    s_i=statesList[i][t]
                    if s_i!=-1:
                        (X,Y)=VizRS.getPlotsLineFine(s_i,th1,th2)
                        plt.scatter(X,Y,s=2)

                fnameTmp=OUTPUT_PATH+'/'+fname+str(ct)+".png"
                fnames.append(fnameTmp)
                plt.savefig(fnameTmp)
            ct=ct+1
            #plt.close()

        with imageio.get_writer(OUTPUT_PATH+'/'+fname+'gif.gif', mode='I',fps=2) as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)

        time_taken=time.time()-time_taken
        print("\tTime Taken: ",time_taken)
        print(">> STATUS: Reachable Sets Visualized!")
