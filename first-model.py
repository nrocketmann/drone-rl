print("importing")
from drone import Drone
import numpy as np
import tensorflow as tf
tf.enable_eager_execution()
from tensorflow.keras.layers import Dense
from scipy.linalg import orth
import time

#define the drone, we'll update its position before each simulation
print("building drone")
agent = Drone(1,5,1,.2)

#input will be position, velocity, angular velocity, and orientation
#vector of length 3+3+3+9=18
print("defining model")
inp = tf.keras.Input(shape=[18],dtype=tf.float32)

#output must have shape 4 (rotor speeds)
#normal dnn
l1 = Dense(36,activation='tanh')(inp)
l2 = Dense(24,activation='tanh')(l1)
l3 = Dense(12,activation='tanh')(l2)
l4 = Dense(4,activation='sigmoid')(l3)

model = tf.keras.Model(inputs=inp,outputs=l4)

#some training constants
#time in seconds, distance in meters for physics
#we can increase these later to make it harder for the drone to fly
dt = .01
sim_updates = 10
sim_time = 2
iterations = int(np.floor(sim_time/(dt*sim_updates)))
print('iterations of python code for one sim: ' + str(iterations))
print('total updates of drone for one sim: ' + str(iterations*(sim_updates)))
max_drone_distance_axis = 1
max_drone_velocity_axis = 2
max_drone_angular_axis = np.pi

alpha = 1e-5
gamma = .98
optimizer = tf.keras.optimizers.Adam(alpha)

#sets up the drone in a random location, orientation, velocity, and rotation
def randomize_drone(dist_max,vel_max,ang_max,sim_agent):
    start_location = np.random.random(size=[3])*dist_max
    start_velocity = np.random.random(size=[3])*vel_max
    start_angular = np.random.random(size=[3])*ang_max
    #graham schmidt to get orientation, assume full rank... hopefully that works
    start_orientation = orth(np.random.random(size=[3,3]))

    sim_agent.setOrientation(start_orientation[0],start_orientation[1])
    sim_agent.setAngular(start_angular)
    sim_agent.setPosition(start_location)
    sim_agent.setVelocity(start_velocity)

def mult_grad(grad,scalar):
    return [scalar*g for g in grad]

def add_grads(grad1,grad2):
    return [g1+g2 for g1,g2 in zip(grad1,grad2)]

def discount_rewards(rewards):
    reward_sum = 0
    discounted = np.zeros(shape=[iterations])
    for i, r in enumerate(reversed(rewards)):
        reward_sum = gamma*reward_sum + r
        discounted[i] = reward_sum
    return discounted


def run_sim():

    #first set up the drone in a random place
    randomize_drone(max_drone_distance_axis,max_drone_velocity_axis,max_drone_angular_axis,agent)

    #we just don't want to have to get this twice each loop
    environment_info = np.reshape(np.array(agent.getVector()),[1,18])

    #rewards for each timestep
    rewards = []

    #main loop for a given simulation
    for i in range(iterations):
        new_speeds = np.array(model(environment_info)).T
        environment_info = np.reshape(np.array(agent.fullIteration(new_speeds,dt,sim_updates)),[1,18])
        rewards.append(1/agent.getLoss())

def randomize_speed_test():
    randomize_drone(max_drone_distance_axis,max_drone_velocity_axis,max_drone_angular_axis,agent)

print('running an episode of the simulation')
t = time.time()
for _ in range(100):
    run_sim()
print(time.time()-t)

