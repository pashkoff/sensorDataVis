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
from KalmanFilter import KalmanFilter

import matplotlib.pyplot as plt
import numpy as np

from twisted.internet import tksupport, reactor

import sys


    
    

def main():
    
    dd = DataDecoder()
#    fil = LowPassFilter()
    fil = KalmanFilter()
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
    
    tk_win = fig.canvas._master
    tksupport.install(tk_win)
    
    def close_ev():
        while True:
            print 'hui'
        
    fig.canvas.mpl_connect('close_event', close_ev)
    
    reactor.run()
    
    pass

if __name__ == '__main__':
    main()
    pass