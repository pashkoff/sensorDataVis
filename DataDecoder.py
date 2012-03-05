'''
Created on 04.03.2012

@author: Pashkoff
'''

import sensor_pb2


from Event import Event

class DataDecoder():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
        self.on_data = Event()
        pass
    
    def __call__(self, data):
        self.__on_data(data)
        pass
        
    def __on_data(self, data):
        if self.on_data.have_any():
            pba = sensor_pb2.Accel()
            pba.ParseFromString(data)
            
            self.on_data(pba)
        pass
    
