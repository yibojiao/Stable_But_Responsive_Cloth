import numpy as np
from particle import particle
from t1spring import t1spring
from t2spring import t2spring

class cloth:

    # length
    N = 0
    # particles
    ps = None
    # t1springs
    t1s = []
    # t2springs
    t2s = []
    # time interval
    h = 0.01
    # activate type2 force
    t2 = False
    # activate damping
    d = True

    def __init__(self, x0, N, t2, d):
        self.N = N
        self.ps = np.empty((N+1, N+1), dtype=np.object)
        self.t2 = t2
        self.d = d
        i = 0
        j = 0
        assert len(x0) == (N+1)**2
        for x in range(len(x0)):
            p = particle(x0[x], np.array([i, j]))
            self.ps[i, j] = p
            if j < self.N:
                j += 1
            else:
                j = 0
                i += 1
    
    def add_springs(self):
        t1set = []
        t2set = []
        N = self.N
        for i in range(N+1):
            for j in range(N+1):
                idx1 = np.array([i, j])
                i1 = int(idx1[1]+(N+1)*idx1[0])

                # add t1 springs
                if i+1 <= N:
                    idx2 = np.array([i+1, j])
                    i2 = int(idx2[1]+(N+1)*idx2[0])
                    t1set.append(np.array([i1, i2]))
                    if j+1 <= N:
                        idx3 = np.array([i+1, j+1])
                        i3 = int(idx3[1]+(N+1)*idx3[0])
                        t1set.append(np.array([i1, i3]))
                    if j-1 >= 0:
                        idx4 = np.array([i+1, j-1])
                        i4 = int(idx4[1]+(N+1)*idx4[0])
                        t1set.append(np.array([i1, i4]))
                if i-1 >= 0:
                    idx2 = np.array([i-1, j])
                    i2 = int(idx2[1]+(N+1)*idx2[0])
                    t1set.append(np.array([i1, i2]))
                    if j+1 <= N:
                        idx3 = np.array([i-1, j+1])
                        i3 = int(idx3[1]+(N+1)*idx3[0])
                        t1set.append(np.array([i1, i3]))
                    if j-1 >= 0:
                        idx4 = np.array([i-1, j-1])
                        i4 = int(idx4[1]+(N+1)*idx4[0])
                        t1set.append(np.array([i1, i4]))
                if j+1 <= N:
                    idx2 = np.array([i, j+1])
                    i2 = int(idx2[1]+(N+1)*idx2[0])
                    t1set.append(np.array([i1, i2]))
                if j-1 >= 0:
                    idx2 = np.array([i, j-1])
                    i2 = int(idx2[1]+(N+1)*idx2[0])
                    t1set.append(np.array([i1, i2]))
                
                # add t2 springs
                if i+2 <= N:
                    idx2 = np.array([i+2, j])
                    i2 = int(idx2[1]+(N+1)*idx2[0])
                    t2set.append(np.array([i1, i2]))
                    if j+2 <= N:
                        idx3 = np.array([i+2, j+2])
                        i3 = int(idx3[1]+(N+1)*idx3[0])
                        t2set.append(np.array([i1, i3]))
                    if j-2 >= 0:
                        idx4 = np.array([i+2, j-2])
                        i4 = int(idx4[1]+(N+1)*idx4[0])
                        t2set.append(np.array([i1, i4]))
                if i-2 >= 0:
                    idx2 = np.array([i-2, j])
                    i2 = int(idx2[1]+(N+1)*idx2[0])
                    t2set.append(np.array([i1, i2]))
                    if j+2 <= N:
                        idx3 = np.array([i-2, j+2])
                        i3 = int(idx3[1]+(N+1)*idx3[0])
                        t2set.append(np.array([i1, i3]))
                    if j-2 >= 0:
                        idx4 = np.array([i-2, j-2])
                        i4 = int(idx4[1]+(N+1)*idx4[0])
                        t2set.append(np.array([i1, i4]))
                if j+2 <= N:
                    idx2 = np.array([i, j+2])
                    i2 = int(idx2[1]+(N+1)*idx2[0])
                    t2set.append(np.array([i1, i2]))
                if j-2 >= 0:
                    idx2 = np.array([i, j-2])
                    i2 = int(idx2[1]+(N+1)*idx2[0])
                    t2set.append(np.array([i1, i2]))
        
        t1set = np.sort(t1set, axis = 1)
        t2set = np.sort(t2set, axis = 1)
        t1set = np.unique(t1set, axis = 0)
        t2set = np.unique(t2set, axis = 0)

        for t1 in t1set:
            p1 = self.ps[int(t1[0]/(N+1)), int(t1[0]%(N+1))]
            p2 = self.ps[int(t1[1]/(N+1)), int(t1[1]%(N+1))]
            spring = t1spring(p1, p2, self.d)
            self.t1s.append(spring)

        for t2 in t2set:
            p1 = self.ps[int(t2[0]/(N+1)), int(t2[0]%(N+1))]
            p2 = self.ps[int(t2[1]/(N+1)), int(t2[1]%(N+1))]
            spring = t2spring(p1, p2, self.d)
            self.t2s.append(spring)
        
    
    def cuff_cloth(self):
        # for i in range(self.N+1):
        #     self.ps[0, i].cuff()
        #     self.ps[i, 0].cuff()
        self.ps[0, 0].cuff()
        self.ps[0, self.N].cuff()
        # self.ps[self.N, self.N].cuff()
        # self.ps[self.N, 0].cuff()
    
    def add_additional_force(self):
        for i in range(self.N+1):
            for j in range(self.N+1):
                self.ps[i,j].add_force([0.001, -0.01, 0])
    
    def time_step(self):
        for i in range(self.N+1):
            for j in range(self.N+1):
                self.ps[i,j].zero_force()
        for t1 in self.t1s:
            t1.compute_t1_force()
        if self.t2:
            for t2 in self.t2s:
                t2.compute_t2_force()
        self.add_additional_force()
        x = np.zeros(((self.N+1)**2, 3))

        for i in range(self.N+1):
            for j in range(self.N+1):
                delta = self.ps[i, j].timestep()
                x[i*(self.N+1)+j] = delta
        return x
    