import numpy as np
import os

os.chdir("/users/nameerhirschkind/CLionprojects/DroneSim")
import drone

# position = np.array([[0,0,0]]).T
# velocity = np.array([[0,0,0]]).T
# angular = np.array([[0,0,0]]).T
#
# orx = np.array([[1,0,0]]).T
# ory = np.array([[0,1,0]]).T

position = np.array([0,0,0])
velocity = np.array([0,0,0])
angular = np.array([0,0,0])

orx = np.array([1,0,0])
ory = np.array([0,1,0])

mass = 1.0
mrf = 5.0
rtorque = 1.0
arm = .3

print('constructing')
x = drone.Drone(mass,mrf,position,velocity,angular,rtorque,orx,ory,arm)
print('constructed')
z = x.getOrientation()
print(z)
x.update(.1)
print(x.getPosition())
print(x.getVelocity())
print(x.getAngular())
print(x.getLoss())