# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 21:30:44 2021

@author: izma
"""

import vrep
import sys
import numpy as np
import math
import matplotlib.pyplot as mlp

PI=math.pi
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

# Python code establish communication with vrep
if clientID!=-1:
    print ('Connected to remote API server')
else:
    print ('Connection not successful')
    sys.exit('Could not connect')  #exit program if connection could not be established.
#define motor handles    
errorcode, left_motor_handle=vrep.simxGetObjectHandle(clientID,"Pioneer_p3dx_leftMotor"
                                                      ,vrep.simx_opmode_oneshot_wait)
errorcode, right_motor_handle=vrep.simxGetObjectHandle(clientID,"Pioneer_p3dx_rightMotor"
                                                      ,vrep.simx_opmode_oneshot_wait)

sensor=h[] #empty list for handles
sensor_val=np.array([]) #empty array for sensor measurements

sensor_loc=np.array([-PI/2, -50/180.0*PI,-30/180.0*PI,-10/180.0*PI,10/180.0*PI,
                     30/180.0*PI,50/180.0*PI,PI/2,PI/2,130/180.0*PI,150/180.0*PI,
                     170/180.0*PI,-170/180.0*PI,-150/180.0*PI,-130/180.0*PI,-PI/2]) 

#for loop to retrieve sensor arrays and initiate sensors
for x in range(1,16+1):
        errorcode,sensor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor'+str(x),vrep.simx_opmode_oneshot_wait)
        sensor_h.append(sensor_handle) #keep list of handles        
        errorcode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor_handle,vrep.simx_opmode_streaming)                
        sensor_val=np.append(sensor_val,np.linalg.norm(detectedPoint)) #get list of values
        

t = time.time()

#LOOPING CODE AND ROBOT CONTROLLER 
while (time.time()-t)<60:
    #Loop Execution
    sensor_val=np.array([])    
    for x in range(1,16+1):
        errorcode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor_h[x-1],vrep.simx_opmode_buffer)                
        sensor_val=np.append(sensor_val,np.linalg.norm(detectedPoint)) #get list of values

    
    #controller specific
    sensor_sq=sensor_val[0:8]*sensor_val[0:8] #square the values of front-facing sensors 1-8
        
    min_ind=np.where(sensor_sq==np.min(sensor_sq))
    min_ind=min_ind[0][0]
    
    if sensor_sq[min_ind]<0.2:
        steer=-1/sensor_loc[min_ind]
    else:
        steer=0
            
    
    v=1	#forward velocity
    kp=0.5	#steering gain
    vl=v+kp*steer
    vr=v-kp*steer
    print "V_l =",vl
    print "V_r =",vr

    errorcode=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle,vl, vrep.simx_opmode_streaming)
    errorcode=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,vr, vrep.simx_opmode_streaming)


    time.sleep(0.2) #loop executes once every 0.2 seconds (= 5 Hz)

#Post ALlocation
errorcode=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle,0, vrep.simx_opmode_streaming)
errorcode=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0, vrep.simx_opmode_streaming)
    