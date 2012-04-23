'''
Created on 23.04.2012

@author: Pashkoff
'''

from Event import Event

import numpy as np

class LowPassFilter():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
        self.on_data = Event()
        self.acc = np.array([0,0,0])
        pass
    
    def __call__(self, data):
        self.__on_data(data)
        pass
        
    def __on_data(self, pba):
        if self.on_data.have_any():
            k = 0.2
            
            a = np.array([pba.x, pba.y, pba.z])
            
            #self.acc = a * k + self.acc * (1 - k)
            self.acc = self.acc + k*(a - self.acc)
            r = self.acc
            
            class D:
                pass
            d = D()
            d.x = r[0]
            d.y = r[1]
            d.z = r[2]
            
            self.on_data(d)
        pass