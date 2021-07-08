'''
Provides API to visualize various artifacts
'''

import os,sys
import random
import matplotlib.pyplot as plt
PROJECT_ROOT = os.environ['SCHDLR_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *

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
