import vrep
import sys
import numpy as np
import matplotlib.pyplot as mlp

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
# Python code establish communication with vrep
if clientID!=-1:
    print ('Connected to remote API server')
else:
    print ('Connection not successful')
    sys.exit('Could not connect')  #exit program if connection could not be established.
errorcode, left_motor_handle=vrep.simxGetObjectHandle(clientID,"Pioneer_p3dx_leftMotor"
                                                      ,vrep.simx_opmode_oneshot_wait)
errorcode, right_motor_handle=vrep.simxGetObjectHandle(clientID,"Pioneer_p3dx_rightMotor"
                                                      ,vrep.simx_opmode_oneshot_wait)
# Setting actuator velocities
errorcode=vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, 1, vrep.simx_opmode_streaming)
errorcode=vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, 1, vrep.simx_opmode_streaming)

# Reading proximity sensors
errorcode, sensor1=vrep.simxGetObjectHandle(clientID,"Pioneer_p3dx_ultrasonicSensor1"
                                                      ,vrep.simx_opmode_oneshot_wait)
#errorcode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID, sensor1,vrep.simx_opmode_streaming)
errorcode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID, sensor1,vrep.simx_opmode_buffer)
 
 # Retrieve image data from v-rep into Python
errorcode,cam_handle=vrep.simxGetObjectHandle(clientID,"cam1",vrep.simx_opmode_oneshot_wait)

#errorcode, resolution,image=vrep.simxGetVisionSensorImage(clientID,
                                                       #  cam_handle,0,vrep.simx_opmode_streaming)
errorcode, resolution,image=vrep.simxGetVisionSensorImage(clientID,
                                                           cam_handle,0,vrep.simx_opmode_buffer)
 
 # Displaying images with the matplotlib python library
 #im=np.array(image, dtype = np.uint8)
 #im.shape
 #im.resize([resolution[0], resolution[1], 3])