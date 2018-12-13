from __future__ import division

import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import time
from smbus import SMBus
import Adafruit_PCA9685
import subprocess
import math
from math import pi
import psutil
import quadprog
import time
#from .quadrotor_qp.quadprog_solve import qp_q_dot_des
#import os
from numpy import array

# Global Variables
bus = SMBus(1)

p = psutil.Process(os.getpid())

p.nice(-19)
p.cpu_affinity([2])


if __name__ == '__main__':

    SETTINGS_FILE = "RTIMULib"

    print("Using settings file " + SETTINGS_FILE + ".ini")
    if not os.path.exists(SETTINGS_FILE + ".ini"):
        print("Settings file does not exist, will be created")

    s = RTIMU.Settings(SETTINGS_FILE)
    imu = RTIMU.RTIMU(s)

    print("IMU Name: " + imu.IMUName())

    if (not imu.IMUInit()):
        print("IMU Init Failed")
        sys.exit(1)
    else:
        print("IMU Init Succeeded")

    # this is a good time to set any fusion parameters

    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)

    poll_interval = imu.IMUGetPollInterval()
    print("Recommended Poll Interval: %dmS\n" % poll_interval)
    T_no = input("Please input the test no.")
    file_name = 'Black_dog_IMU_data_' + str(T_no) + '.txt'
    f = open(file_name,'w')
    f.close()
    begin = time.time()
    begin_temp = begin
    while 1:
        if imu.IMURead():
	    begin_temp = time.time()
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
	    fusionVel = data["gyro"]
	    Acc = data["accel"]
	    IMU_data =  [fusionPose[0]*180/3.14, fusionPose[1]*180/3.14, fusionPose[2]*180/3.14]
            dIMUdt = [fusionVel[0]*180/3.14, fusionVel[1]*180/3.14, fusionVel[2]*180/3.14]
#	    print [Acc[0], Acc[1], Acc[2]]
	    T = time.time() - begin
	    dT = time.time() - begin_temp
	    print IMU_data[0], IMU_data[1], dT
	    f = open(file_name,'a')
    	    f.write(str(IMU_data[0]) + ',' +str(dIMUdt[0]) + ',' + str(T) +'\n')
f.close()