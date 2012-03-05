'''
Created on 04.03.2012

@author: Pashkoff
'''
from DataDecoder import DataDecoder
from UdpServer import UdpServer
from PlotLine import PlotLine
from Axis import Axis
from Event import Event

import matplotlib.pyplot as plt
import numpy as np


class Filter():
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
    
    

def main():
    
    dd = DataDecoder()
    fil = Filter()
    serv = UdpServer()
    
    fig = plt.figure()
    
    dd.on_data.add(fil)
    
    rows = 3
    cols = 1
    i = 1
    for f in ('x', 'y', 'z'):
        ax = Axis(fig, [rows, cols, i])
        dd.on_data.add(ax)
        
        line = PlotLine(f,color='b')
        dd.on_data.add(line)
        ax.add_line(line)
        
        linef = PlotLine(f, color='r')
        fil.on_data.add(linef)
        ax.add_line(linef)
        
        i = i + 1
        pass
    
    serv.on_read.add(dd)
    
    
    
    plt.ion()
    plt.plot()
    plt.draw()
    
    serv.run()
    
    pass

if __name__ == '__main__':
    main()
    pass