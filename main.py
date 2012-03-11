'''
Created on 04.03.2012

@author: Pashkoff
'''
import sys

from DataDecoder import DataDecoder
from UdpServer import UdpServer
from PlotLine import PlotLine
from Axis import Axis
from Event import Event

import matplotlib.pyplot as plt
import numpy as np

class DataSaver:
    def __init__(self):
        self.d = list()
    
    def __call__(self, data):
        self.__on_data(data)
        pass
    
    def __on_data(self, pba):
        a = np.array([pba.x, pba.y, pba.z])
        self.d.append(a)
        
        print len(self.d) 
        
        if len(self.d) >= 1000:
            np.savetxt('data1000', self.d)
            sys.exit()


def main():
    
    dd = DataDecoder()
    serv = UdpServer()
    
    saver = DataSaver()
    dd.on_data.add(saver)
    
    serv.on_read.add(dd)
    
    serv.run()
    
    pass

if __name__ == '__main__':
    main()
    pass