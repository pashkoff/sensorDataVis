'''
Created on 04.03.2012

@author: Pashkoff
'''

import asyncore
import socket
from Event import Event


class UdpServer(asyncore.dispatcher):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
        self.on_read = Event()
        
        asyncore.dispatcher.__init__(self)
        
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(('', 48912))
                
        pass
    
    def handle_connect(self):
        asyncore.dispatcher.handle_connect(self)
        pass
    
    def handle_read(self):
        data, addr = self.recvfrom(2048)
        self.on_read(data)
        pass
    
    
    def handle_write(self):
        asyncore.dispatcher.handle_write(self)
        pass
    
    
    def run(self):
        asyncore.loop()
        pass
    
    pass

