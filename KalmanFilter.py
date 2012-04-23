'''
Created on 23.04.2012

@author: Pashkoff
'''

from Event import Event

import numpy as np

class Channel():
    def __init__(self):
        self.Q = 1e-5
        self.xhat = 0
        self.P = 1
        self.xhatminus = 0
        self.Pminus = 0
        self.K = 0
        self.R = 0.1 ** 4
        pass
    
    
    def step(self, z):
        self.xhatminus = self.xhat
        
        self.Pminus = self.P + self.Q
        
        self.K = self.Pminus / (self.Pminus + self.R)
        self.xhat = self.xhatminus + self.K * (z - self.xhatminus)
        self.P = (1 - self.K) * self.Pminus
        
        return self.xhat

class KalmanFilter():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
        self.on_data = Event()
        self.ch = [Channel(), Channel(), Channel()]
        
        pass
    
    def __call__(self, data):
        self.__on_data(data)
        pass
        
    def __on_data(self, pba):
        if self.on_data.have_any():
            
            a = np.array([pba.x, pba.y, pba.z])
            
            r = list()
            for i in range(3):
                z = self.ch[i].step(a[i])
                r.append(z)
                pass
            
            class D:
                pass
            d = D()
            d.x = r[0]
            d.y = r[1]
            d.z = r[2]
            
            self.on_data(d)
        pass