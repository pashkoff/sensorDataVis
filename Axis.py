'''
Created on 04.03.2012

@author: Pashkoff
'''

import matplotlib.pyplot as plt
from matplotlib import animation
from Event import Event
import itertools

class Axis():
    '''
    classdocs
    '''

    def __init__(self, fig, subplot, maxt=1, dt=0.01, ylims = (-1, 1)):
        '''
        Constructor
        '''
        
        self.maxt = maxt
        self.dt = dt
        self.subplot = subplot
        self.ylims = list(ylims)
        
        
        self.tdata = [0]
        
        self.ax = fig.add_subplot(*self.subplot)
        self.ylims_ch()
        self.ax.set_xlim(0, self.maxt)
        self.ax.grid()
        
        self.on_data = Event()
        self.__on_line_upd = Event()
        self.__on_line_rst = Event()
        self.need_stop = False
        
        self.anim = animation.FuncAnimation(fig, self.update, itertools.count, blit=True, event_source=self)
        
        
        
        pass
    
    def __call__(self, *args, **kwargs):
        self.on_data()
        pass
    
    def add_line(self, line):
        self.ax.add_line(line.get_line())
#        line.on_data.add(self)
        line.on_min_changed.add(self.ymin_ch)
        line.on_max_changed.add(self.ymax_ch)
        self.__on_line_upd.add(line.update)
        self.__on_line_rst.add(line.reset)
        
    def rem_line(self, line):
        self.__on_line_rst.remove(line.reset)
        self.__on_line_upd.remove(line.update)
        line.remove()
    
    def update(self, y):
        
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt: # reset the arrays
            self.tdata = [self.tdata[-1]]
            
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            
            self.ylims[0] = self.ylims[0]/2
            self.ylims[1] = self.ylims[1]/2
            self.ylims_ch()
            self.__on_line_rst(self.tdata)
            
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        
        lines = self.__on_line_upd(self.tdata)
        
        return lines
    
    def ymin_ch(self, val):
        if self.ylims[0] > val:
            self.ylims[0] = val
            self.ylims_ch()
    
    def ymax_ch(self, val):
        if self.ylims[1] < val:
            self.ylims[1] = val
            self.ylims_ch()
    
    def ylims_ch(self):
        self.ax.set_ylim(self.ylims)
    
    def add_callback(self, clb):
#        print "add_callback", clb
        self.on_data.add(clb)

    def remove_callback(self, clb):
#        print "remove_callback", clb
        self.on_data.remove(clb)
        pass
    
    def start(self):
        pass
    
    def stop(self):
        pass
    
