import numpy as np

class particle:

    def __init__(self, pos, idx):
        # material space position
        self.X = pos.copy()
        # physical space position
        self.x = pos.copy()
        # acceleration
        self.a = np.zeros((3,))
        # velocity
        self.v = np.zeros((3,))
        # mass inverse
        self.m = 1e5
        # force on this particle
        self.f = np.zeros((3,))
        # time step
        self.h = 0.002
        # index on the cloth
        self.idx = idx
    
    def cuff(self):
        self.m = 0
    
    def timestep(self):
        self.a = self.m * self.f
        self.v += self.h * self.a
        self.x += self.h * self.v
        return self.h * self.v

    def add_force(self, F):
        self.f += F
    
    def zero_force(self):
        self.f = np.zeros((3,))

    def getf(self):
        return self.f
    
    def getv(self):
        return self.v
    
    def geta(self):
        return self.a
    
    def getm(self):
        return self.m

    def getX(self):
        return self.X

    def getx(self):
        return self.x
    
    def setx(self, x):
        self.x = x

    