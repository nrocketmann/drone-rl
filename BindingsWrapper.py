import numpy as np
from drone import Drone

#THIS IS PURELY FOR VISUALIZATION
#IT'S TOO SLOW TO USE FOR TRAINING

class Simulator:
    def __init__(self,drone_class): #takes a drone class already built as input
        self.d = drone_class

    #model must be a function
    def animate(self,model, dt, steps):
        self.d.setPosition(np.array([0,0,0]))
        self.d.setVelocity(np.array([0,0,0]))
        self.d.setAngular(np.array([0,0,0]))
        self.d.setOrientation(np.array([[1,0,0],[0,1,0],[0,0,1]]))
        