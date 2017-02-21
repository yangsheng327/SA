# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Downhill simplex with simulated annealing

import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

class DSSA:
    
    def __init__(self, lossfun, init_para, coei=[1,2,1./2,1./2], k=1):
        self.fun = lossfun
        self.df = init_para.shape[1]
        self.para = np.zeros([self.df+1, self.df])
        self.para[:,:] = init_para[:,:]
        self.loss = np.zeros(self.df+1)
        self.alpha = coei[0]
        self.gama = coei[1]
        self.rou = coei[2]
        self.delta = coei[3]
        self.k = k #energy constant
        for n in range(df+1):
            self.loss[n] = self.fun(self.para[n,:])
            
#    def prob(self, target, opponent, T): #Boltzman distribution
#        return 1./(1+np.exp((target-opponent)/self.k/T))
        
    def order(self):#sort para based on loss function
        sort_id = np.argsort(self.loss)
        self.loss = self.loss[sort_id]
        self.para = self.para[sort_id,:]
        self.centr = np.mean(self.para[:-1,:], axis=0)
        self.ref =  self.centr + self.alpha*(self.centr-self.para[-1,:])
        self.ref_loss = self.fun(self.ref)
    
    def reflect(self):#reflection
        self.para[-1,:] = self.ref
        self.loss[-1] = self.ref_loss
          
    def expand(self):#expansion
        self.exp = self.centr + self.gama*(self.ref-self.centr)
        self.exp_loss = self.fun(self.exp)
        if self.exp_loss<self.ref_loss:
            self.para[-1,:] = self.exp
            self.loss[-1] = self.exp_loss
        else:
            self.para[-1,:] = self.ref
            self.loss[-1] = self.ref_loss
    
    def contract(self):
        self.contr = self.centr + self.rou*(self.para[-1,:]-self.centr)
        self.contr_loss = self.fun(self.contr)
        if self.contr_loss<self.loss[-1]:
            self.para[-1,:] = self.contr
            self.loss[-1] = self.contr_loss
        else:#shrink
            for n in range(df):
                self.para[n+1:,:] = self.para[0,:] + \
                    self.delta*(self.para[n+1:,:]-self.para[0,:])
                self.loss[n+1] = self.fun(self.para[n+1,:])
               
    def fit(self, iter_num):
        for i in range(iter_num):
            self.order()
            if self.ref_loss<self.loss[-2] and self.ref_loss>self.loss[0]:
                self.reflect()
            elif self.ref_loss<=self.loss[0]:
                self.expand()
            else:
                self.contract()
    
#def loss(x):
#    r = np.sqrt(sum(x**2))# + np.random.uniform(0,0.5)
#    return -(np.sin(r)/r)
##def loss(x):
##    return sum(x**2)
#
#    
#    
#    
#df = 2#dimension of freedom
#x0 = np.random.randint(-20,20, [df + 1, df])
#ds = DSSA(loss, x0)
#ds.fit(50)
#print(ds.para)
#print(ds.loss)
#print(ds.centr)