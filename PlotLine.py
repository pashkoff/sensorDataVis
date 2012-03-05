'''
Created on 04.03.2012

@author: Pashkoff
'''

from collections import deque
from Event import Event
from matplotlib.lines import Line2D


class PlotLine():
    '''
    classdocs
    '''


    def __init__(self, field, color):
        '''
        Constructor
        '''
        
        self.field = field
        
        self.ydata = []
        self.saved_ydata = deque()
        
        self.line = Line2D([], [], color=color)
        
        self.on_data = Event()
        
        self.on_min_changed = Event()
        self.on_max_changed = Event()
        
        self.min = 0
        self.max = 0
        
        pass
    
    def __call__(self, acc):
        val = getattr(acc, self.field)
        self.__on_data(val)
        pass
    
    def __on_data(self, val):
        
        self.saved_ydata.append(val)
        if val > self.max:
            self.max = val
            self.on_max_changed(val)
            pass
        if val < self.min:
            self.min = val
            self.on_min_changed(val)
            pass
        
        self.on_data()
        
        pass
    
    def update(self, tdata):
        
        assert len(self.ydata) <= len(tdata)
        
        while len(self.ydata) < len(tdata):
            if len(self.saved_ydata) == 0:
                self.ydata.append(0)
            else:
                self.ydata.append(self.saved_ydata.popleft())
                pass
            pass
        
        self.line.set_data(tdata, self.ydata)
        return self.line
    
    def reset(self, tdata):
        self.ydata = [self.ydata[-1]]
        self.max = self.min = self.ydata[-1]
        self.on_max_changed(self.max)
        self.on_min_changed(self.min)
        pass
    
    def get_line(self):
        return self.line
    
    pass
