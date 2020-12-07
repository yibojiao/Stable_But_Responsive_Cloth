import numpy as np
from particle import particle

class t1spring:

    # particle 1
    p1 = None
    # particle 2
    p2 = None
    # natural length
    L = 0
    # stiff constant
    k = 1.5
    # activate damping
    d = True

    def __init__(self, p1, p2, d):
        self.p1 = p1
        self.p2 = p2
        self.d = d
        self.L = np.linalg.norm(p1.getX() - p2.getX())

    def compute_t1_force(self):
        x = self.p2.getx() - self.p1.getx()
        l = np.linalg.norm(x)
        self.f = 0
        if l > self.L:
            f = self.k * (l - self.L) * (x/l)
            if self.d:
                self.damp(f)
            self.p1.add_force(f)
            self.p2.add_force(-f)
            self.f = f
    
    def damp(self, f):
        v1 = self.p1.getv()
        v2 = self.p2.getv()
        f += 0.0001*(v2 - v1)