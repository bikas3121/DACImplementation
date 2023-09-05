#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:35:58 2023

@author: bikashadhikari
"""
from scipy import signal
import statistics
class signalProcessing:
    
    def __init__(self, N, t, ref, b, a):
        self.N = N  # prediction horizon
        self.t = t  # simulation time
        self.ref = ref # reference signal
        self.b =b  # transfer function numberator
        self.a = a # transfer function denominator
    
    @property
    def referenceFilter(self):
        filteredReference = signal.lfilter(self.b, self.a, self.ref)
        return filteredReference[0:len(self.t)]
    
    def signalFilter(self, sig):
        sig = sig[0:len(self.t)]
        filteredSignal = signal.lfilter(self.b, self.a, sig)
        errorWRTreference = self.referenceFilter-filteredSignal
        varianceError = round(statistics.variance(errorWRTreference),4)
        return [filteredSignal, errorWRTreference, varianceError]
    
    # def errorVar(self):
        
        
        