#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:32:47 2023

@author: bikashadhikari
"""

#main file
import numpy as np
import itertools


class ClosedFormMPC:
    # Initialized the class with 
        # N - prediction horizon
        # A B,C,D - state matrices obtained after conversion of the filter transfer function into state space representation
        # h - impulse response of the filter (low pass)
        # Q - qunatization levels. 
    
    
    def __init__(self, N, A, B, C, h):
        self.N = N  # prediction horizon
        self.A = A  # state matrix of the lowpass filter
        self.B = B # input matrix
        self.C = C  # output matrix of low pass filter
        self.h = h  # impulse response of the low pass filter
        # self.Q = Q  # quantization levels
        
    
    
    @property
    def Tau(self):
        Tau = self.C
        for i in range(1,self.N):
            A_ast = np.linalg.matrix_power(self.A, i)
            Tau_i = np.matmul(self.C, A_ast)
            Tau = np.vstack((Tau, Tau_i[0]))
        return Tau
    
    @property
    def Psi(self):
        Psi = np.zeros(shape = (self.N,self.N))
        for i in range(0,self.N):    
            k = i
            for j in range(0, i+1):
                Psi[i][j] = self.h[k]
                k = k-1
        return Psi
        
    # @property
    # Perform and return scalar quantization level into vector quantization levels
    # Returns the cartesian product of the quantization leves with N x |U|^N matrix
    def vectorQuantizationLevels(self, Q):
        cartU = list(itertools.product(Q,repeat=self.N))
        lenU = len(cartU)

        # list to matrix
        Un = np.zeros((self.N,len(cartU)))
        for i in range(lenU):
            c1 = cartU[i]
            for j in range(self.N):
                Un[j,i] = c1[j] 
        return Un
            

    def cfQuantizer(self, x0, Tf, Un_tilde,ref):
        # INPUTS:
            # x0 : initial condition
            # Tf: total simulation time
            # Un_tilde : Transformed vector quantization levels
            
        # OUTPUT: returns the closed quantization levels
            
        # Un_tilde = np.matmul(Psi, Un)
        lenU = Un_tilde.shape[1]
        u_mhoq = []
        x = []
        x.append(x0)
        for i in range(0,Tf):
            x_k = np.reshape(x[i], (2,1))
            a_k = np.reshape(ref[i:i+self.N], (self.N,1))
            sm = np.matmul(self.Psi,a_k) + np.matmul(self.Tau, x_k)
            sm = np.reshape(sm, (1,self.N))
        
            # nearest neighbor quatnizer
            norm_err = []
            for j in range(0,lenU):
                norm_err_j = np.linalg.norm(sm- Un_tilde[:,j])
                norm_err = np.append(norm_err, norm_err_j)
                
            min_err = np.min(norm_err)
            index = np.where(norm_err == min_err)  # find the index with minimum error
            Un_opt = Un_tilde[:,index[0]]    
            
            Un_opt = np.reshape(Un_opt, (self.N,1))
        
            u_opt_i = np.matmul(np.linalg.inv(self.Psi),Un_opt)
        
            u_mhoq = np.hstack((u_mhoq, u_opt_i[0]))
            # u_mhoq = np.append(u_mhoq, u_opt_i[0])
        
        
            # state evolution
            # x1_0 = np.reshape(x[i,:], (2,1))
            
            u1_0 = ref[i] - u_mhoq[i] 
            x_i = np.matmul(self.A, x_k) + self.B*u1_0
            x = np.vstack((x, np.reshape(x_i, (1,2))))
        return u_mhoq

