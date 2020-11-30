import numpy as np
from polysinc import polysinc

class t2spring:

    # particle 1
    p1 = None
    # particle 2
    p2 = None
    # natural length
    L = 0
    # sinc polynomial
    poly = polysinc().p
    # buckling constant
    k = 0.001
    # constant
    c = 1

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.L = np.linalg.norm(p1.getX() - p2.getX())
    
    def κ(self, x):
        ratio = x / self.L
        assert ratio <= 1 and ratio >= 0
        sinc = self.poly[0]*(ratio**5)+\
               self.poly[1]*(ratio**4)+\
               self.poly[2]*(ratio**3)+\
               self.poly[3]*(ratio**2)+\
               self.poly[4]*(ratio)+self.poly[5]
        k = sinc * (2 / self.L)
        return k

    def compute_t2_force(self):
        x = self.p2.getx() - self.p1.getx()
        l = np.linalg.norm(x)
        self.f = 0
        if l < self.L:
            κ = self.κ(l)
            kl = κ*self.L/2
            fb = self.k* (κ**2)\
                * (1 / (np.cos(kl) - np.sinc(kl)))

            if fb < self.c*(l-self.L):
                fb = self.c*(l-self.L)

            f = fb * (x/l)
            self.damp(f)
            self.p1.add_force(f)
            self.p2.add_force(-f)
            self.f = f
            
    def damp(self, f):
        v1 = self.p1.getv()
        v2 = self.p2.getv()
        f += 0.0001*(v2 - v1)