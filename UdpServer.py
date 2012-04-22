'''
Created on 04.03.2012

@author: Pashkoff
'''

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from Event import Event


class UdpServer(DatagramProtocol):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
        self.on_read = Event()
        
        
        reactor.listenUDP(48912, self)
        
        pass
    
    
    def datagramReceived(self, data, (host, port)):
        self.on_read(data)
        pass
    
    
    pass

