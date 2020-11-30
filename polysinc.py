import numpy as np
import matplotlib.pyplot as plt

class polysinc:
     
    # polynomial parameters
    p = None
    # degree
    d = 5

    def __init__(self):
        x = np.linspace(0, 1, 1000)
        y = np.sinc(x)
        p = np.polyfit(y, x, self.d)
        f = np.polyval(p, x)
        f = self.scale_range(f, 0, 1)
        p = np.polyfit(x, f, 5)
        self.p = p

    def scale_range (self, f, fmin, fmax):
        f += -(np.min(f))
        f /= np.max(f) / (fmax - fmin)
        f += fmin
        return f
    
    def __illustration(self):
        # linspace of sinc function 
        x = np.linspace(0, 1, 1000)
        y = np.sinc(x)
        # take inverse of sinc function
        # get polynomial fit
        p = np.polyfit(y, x, 5)
        # inverse of sinc
        f = np.polyval(p, x)
        f = self.scale_range(f, 0, 1)
        # re-fit the polynomial
        p = np.polyfit(x, f, 5)
        # plot sinc
        plt.plot(x, y)
        # plot sinc-1
        plt.plot(x, f)
        print('Polynomial function approximates of sinc^-1 is: ', p)
