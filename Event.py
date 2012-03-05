'''
Created on 04.03.2012

@author: Pashkoff
'''

class Event():
    '''
    classdocs
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        
        self.clbs = set()
        
    def add(self, clb):
        self.clbs.add(clb)
        pass
    
    def remove(self, clb):
        self.clbs.remove(clb)
        pass
    
    def __call__(self, *args, **kwargs):
        res = list()
        for c in self.clbs:
            r = c(*args, **kwargs)
            res.append(r)
            pass
        return res
    
    def have_any(self):
        return len(self.clbs) > 0
    
    pass

