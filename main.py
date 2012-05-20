'''
Created on 04.03.2012

@author: Pashkoff
'''
from DataDecoder import DataDecoder
from UdpServer import UdpServer
from PlotLine import PlotLine
from Axis import Axis
from Event import Event
from LowPassFilter import LowPassFilter

import matplotlib.pyplot as plt
import numpy as np

from twisted.internet import tksupport, reactor

import sys


class LevelFilter():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
        self.on_data = Event()
        self.prev = np.array([0,0,0])
        pass
    
    def __call__(self, data):
        self.__on_data(data)
        pass
        
    def __on_data(self, pba):
        if self.on_data.have_any():
            k = 0.2
            
            a = np.array([pba.x, pba.y, pba.z])
            
            def f(x, px, level):
                return x if abs(x - px) > level else px
            
            for i in range(3):
                self.prev[i] = f(a[i], self.prev[i], 0.8)
            
            r = self.prev
            
            class D:
                pass
            d = D()
            d.x = r[0]
            d.y = r[1]
            d.z = r[2]
            
            self.on_data(d)
        pass
    pass


def main():
    
    dd = DataDecoder()
    level = LevelFilter()
    fil = LowPassFilter()
    serv = UdpServer()
    
    fig = plt.figure()
    
    dd.on_data.add(fil)
    fil.on_data.add(level)
    
    rows = 3
    cols = 1
    i = 1
    for f in ('x', 'y', 'z'):
        ax = Axis(fig, [rows, cols, i], dt = 1, maxt = 100)
        dd.on_data.add(ax)
        
        line = PlotLine(f,color='b')
        dd.on_data.add(line)
        ax.add_line(line)
        
        linef = PlotLine(f, color='r')
        fil.on_data.add(linef)
        ax.add_line(linef)
        
        linef = PlotLine(f, color='g')
        level.on_data.add(linef)
        ax.add_line(linef)
        
        i = i + 1
        pass
    
    serv.on_read.add(dd)
    
    plt.ion()
    plt.plot()
    plt.draw()
    
    tk_win = fig.canvas._master
    tksupport.install(tk_win)
    
    def close_ev():
        while True:
            print 'bye'
        
    fig.canvas.mpl_connect('close_event', close_ev)
    
    reactor.run()
    
    pass

if __name__ == '__main__':
    main()
    pass