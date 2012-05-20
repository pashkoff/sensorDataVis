'''
Created on 23.04.2012

@author: Pashkoff
'''

import sys

from Event import Event

import numpy as np
from numpy import dot, sum, tile, linalg, log, exp, pi, array, eye, zeros, diag
from numpy.linalg import inv, det
 
def kf_predict(X, P, A, Q, B, U):
    X = dot(A, X) + dot(B, U)
    P = dot(A, dot(A, A.T)) + Q
    return (X, P)

def gauss_pdf(X, M, S): 

    if M.shape[1] == 1: 
        DX = X - np.tile(M, X.shape[1])   
        E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0) 
        E = E + 0.5 * M.shape[0] * log(2 * pi) + 0.5 * log(det(S)) 
        P = exp(-E) 
    elif X.shape[1] == 1: 
        DX = tile(X, M.shape[1])- M   
        E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0) 
        E = E + 0.5 * M.shape[0] * log(2 * pi) + 0.5 * log(det(S)) 
        P = exp(-E) 
    else: 
        DX = X-M   
        E = 0.5 * dot(DX.T, dot(inv(S), DX)) 
        E = E + 0.5 * M.shape[0] * log(2 * pi) + 0.5 * log(det(S)) 
        P = exp(-E) 
 
    return (P[0],E[0]) 

def kf_update(X, P, Y, H, R):
    IM = dot(H, X) 
    IS = R + dot(H, dot(P, H.T)) 
    K = dot(P, dot(H.T, inv(IS))) 
    X = X + dot(K, (Y-IM)) 
    P = P - dot(K, dot(IS, K.T)) 
    LH = gauss_pdf(Y, IM, IS) 
    return (X,P,K,IM,IS,LH) 

class KalmanFilter():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
        self.on_data = Event()
        
        self.X = np.array([[0.0], [0.0], [0.0]]) 
        self.P = eye(self.X.shape[0]) * 0.1 ** 4  
        self.A = np.array([[1., 0.,  0.], [0., 1., 0.], [0., 0., 1.]]) 
        self.Q = eye(self.X.shape[0]) * 0.0001 
        self.B = eye(self.X.shape[0]) 
        self.U = zeros((self.X.shape[0], 1))
        self.H = eye(self.X.shape[0]) 
        self.R = eye(self.X.shape[0]) * 5 ** 1 
        
        print self.X
        print self.P
        print self.A
        print self.Q
        print self.B
        print self.U
        print self.H
        print self.R
        
#        sys.exit()
        
        
        pass
    
    def __call__(self, data):
        self.__on_data(data)
        pass
        
    def __on_data(self, pba):
        if self.on_data.have_any():
            
            Y = np.array([[pba.x], [pba.y], [pba.z]])
            
            (self.X, self.P) = kf_predict(self.X, self.P, self.A, self.Q, self.B, self.U)
            (self.X, self.P, K, IM, IS, LH) = kf_update(self.X, self.P, Y, self.H, self.R)
            
            print (K, IM, IS, LH)
             
            class D:
                pass
            d = D()
            d.x = self.X[0]
            d.y = self.X[1]
            d.z = self.X[2]
            
            self.on_data(d)
        pass