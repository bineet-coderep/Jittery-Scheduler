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

class Viz:

    def vizAllTraj(trajs,fname="all_trajectories"):
        '''
        Visualize all trajectories in trajs.

        - Initial set marked with a green circle.
        - `trajs[0]` is all miss --- marked in red.
        - `trajs[-1]` is not miss --- marked in blue.
        - Rest of the trajectories are in random color.
        '''

        # Mark Initial Set
        plt.figure()
        plt.scatter(trajs[-1][0][0],trajs[-1][1][0], s=120, facecolors='none', edgecolors='g')

        # Rest of the trajectories
        for i in range(1,len(trajs)-1):
            plt.plot(trajs[i][0][:],trajs[i][1][:],linestyle='-',markersize=3,marker='o',linewidth=0.5)

        # Print 4 Random Trajectories: To be deleted later
        rTrajs=[random.randint(0,len(trajs)) for i in range(0)]
        for j in rTrajs:
            plt.plot(trajs[j][0][:],trajs[j][1][:],linestyle='--',markersize=4,marker='o',color='k',linewidth=1)


        # All Miss Trajectory
        plt.plot(trajs[0][0][:],trajs[0][1][:],linestyle='--',markersize=5,marker='o',color='r',label='All Miss',linewidth=2)

        # No Miss Trajectory
        plt.plot(trajs[-1][0][:],trajs[-1][1][:],linestyle='--',markersize=5,marker='o',color='b',label='No Miss',linewidth=2)


        plt.legend()
        plt.savefig(OUTPUT_PATH+'/'+fname)
        plt.close()

    def vizCompTraj(allTrajs,trajs,fname="compare_all_trajectories"):
        '''
        Visualize all trajectories in trajs.

        - Initial set marked with a green circle.
        - Rest of the trajectories are in random color.
        - Visualize `trajs`
        '''

        # Mark Initial Set
        plt.figure()
        plt.scatter(allTrajs[-1][0][0],allTrajs[-1][1][0], s=120, facecolors='none', edgecolors='g')

        # Rest of the trajectories
        for i in range(1,len(allTrajs)-1):
            plt.plot(allTrajs[i][0][:],allTrajs[i][1][:],linestyle='-',markersize=3,marker='o',color='cyan',linewidth=0.5)

        for (traj,lb) in trajs:
            if lb=="All Miss" or lb=="All Hit":
                plt.plot(traj[0][:],traj[1][:],linestyle='-',markersize=5,marker='o',label=lb,linewidth=3)
            else:

                plt.plot(traj[0][:],traj[1][:],linestyle='--',markersize=5,marker='o',label=lb,linewidth=2)



        plt.legend()
        plt.savefig(OUTPUT_PATH+'/'+fname)
        plt.close()


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

        for a in range(900):
            an=a/10
            if an==90:
                model.addConstr(X==0,"Angle")
            else:
                m=math.tan(math.radians(an))
                model.addConstr(Y==m*(X),"Angle")
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

    def vizAllRS(trajs,randTrajs,fname="all_trajectories"):
        th1=0
        th2=1
        plt.figure()
        plt.plot([1],[1],color='m',label="Random ("+str(len(randTrajs))+")")
        for traj in randTrajs:
            for rs in traj:
                (X,Y)=VizRS.getPlotsLineFine(rs,th1,th2)
                plt.scatter(X,Y,color='m',s=0.5)

        colors=['g','b','k','y','r']
        cCount=0
        for (traj,lb) in trajs:
            plt.plot([1],[1],color=colors[cCount],label=lb)
            for rs in traj:
                #print(rs)
                (X,Y)=VizRS.getPlotsLineFine(rs,th1,th2)
                plt.scatter(X,Y,color=colors[cCount],s=0.5)
            cCount=cCount+1

        plt.legend()
        plt.savefig(OUTPUT_PATH+'/'+fname)
        plt.close()
