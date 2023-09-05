#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 10:25:01 2023

@author: bikashadhikari
"""
# %%
import numpy as np
from scipy  import signal
# import statistics
# import matplotlib.pyplot as plt
import csv
# import random


# custom modules
import DirectQantization as dq
import gurobiMPC as gMPC  # solve the MPC using gurobi without INL feedback
import gurobiMPCINL as gMPCINL  # solve the MPC using gurobi with INL feedback

from cfMPC import ClosedFormMPC # solve the closed from MPC problem
from signalProcessing import signalProcessing



# %% 
N = 2    # prediction horizon 
    
# Input Signal Properties
freq = 5  # reference/ input signal frequency

nob = 8   # number of bits
amp = 2**nob  # signal peak-to-peak amplitude 

# %% Initial Paramters

#filter parameters
f_c =1e2 # cutoff frequency
f_s = 1e3;  # sampling frequency
Wn = f_c / (f_s / 2)

# sampling 
T_s = 1/f_s; # sampling rate
t_end = 1; # time vector duration
t = np.arange(0,t_end,T_s)  # time vector


#  Reference signal
t1 = np.arange(0,1.1,T_s )

ref = 1/2*(amp*np.sin(2*np.pi*freq*t1)) + amp/2  # ref signal

# ref = np.random.uniform(-8.5, 7.5, len(t1))


# %% Filter parametres
# Butterworth Filter properties 
b, a = signal.butter(2, Wn, 'low')
butter = signal.dlti(*signal.butter(2, Wn,'low'))
w, h = signal.dimpulse(butter, n = 10)  #w - angular frequency, h= frequency response
h = h[0]

# Transfer function to StateSpace
A, B, C, D = signal.tf2ss(b,a)

# %% Quatantizer Parameters
# Q = np.arange(-8, 8,1 )
Q =  np.arange(0, int(amp)+1,1)  #quantizer levels

# INL 
# Read INL from the saved file for the reproduciblity of the simulation results.
INL = []
with open ('INL.txt') as f:
    # w = [float(x) for x in next(f).split()]
    array = []
    for line in f: # read rest of lines
        array = [float(x) for x in line.split()]
        INL.append(array[0]) # multiplied by 3 to increase the size of the INL size. 
        
INL = INL[0:len(Q)]
INL[0] = 0  

# add INL to the uniform quantizer levels to generate a non-ideal quantizer
U = Q + INL

# %%  Nearest neighbor(Direct)  Quantization 

# Direct quantization with uniform quatizer levels
u_direct = dq.DirectQuantization(Q, ref)

# Direct quantization with non-uniform quatizer levels
# Direct quant + INL
u_direct_INL = dq.DirectQuantization(U, ref)

# %% Moving Horizon Closed From Solution Parameters
# mpc1 = ClosedFormMPC(N, A, B, C, h)
# Tau = mpc1.Tau
# Psi = mpc1.Psi
# x0 = [1,1]
# MHOQ without INL
# Un = mpc1.vectorQuantizationLevels(Q)
# transformation of the constraint space
# Un_tilde = np.matmul(Psi, Un)


# Tf = len(t)   # reference signal length
# u_mhoq = mpc1.cfQuantizer(x0, Tf, Un_tilde, ref)
# u_mhoq = dq.DirectQuantization(Q, u_mhoq)

# # % mhoq with INL:
# Un_INL = mpc1.vectorQuantizationLevels(U)
# Un_tilde_INL = np.matmul(Psi, Un_INL)
# u_mhoq_INL = mpc1.cfQuantizer(x0, Tf, Un_tilde_INL, ref)
# u_mhoq_INL = dq.DirectQuantization(U, u_mhoq)

# %% MPC- Gurobi 
x0 = [1,1]      # initial condition
x0 = np.reshape(x0,(2,1))   # reshaping into column vector

u_mpc = gMPC.MPC(x0, N, ref, Q, A, B, C, D, t) #solve the MPC problem with Gurobi. 

u_mpc = dq.DirectQuantization(Q, u_mpc)   # Quantization using Unifrom DAC
u_mpc1 = dq.DirectQuantization(U, u_mpc)  # Quantization using Non-unifrom DAC

# %% MPC Gurobi  with INL Feedback

u_mpc_INL = gMPCINL.MPC(x0, N, ref, A, B, C, D, t, Q, INL)
u_mpc_INL = dq.DirectQuantization(U, u_mpc_INL)


# %%  Write data into file.
headerlist = ['Time', 'Reference', 'Direct (Unifrom)', 'Direct(Non-uniform)', 'MPC(Unifrom)', 'MPC(Non-Uniform)', 'MPC(Non-Unifrom with  INL Feedback)']
# headerlist = ['Time', 'Reference', 'Direct', 'Direct-INL', 'MPC', 'MPC-INL (w/o INL)',  'MPC with INL']
with open('unfiltered_simulationresult.csv','w') as f:
    writer = csv.writer(f, delimiter ='\t')
    writer.writerow(headerlist)
    writer.writerows(zip(t, ref, u_direct, u_direct_INL,  u_mpc, u_mpc1,  u_mpc_INL))


# %% Signal Processing

sgp = signalProcessing(N, t, ref, b, a)

# Filtered reference signal
filtered_reference = sgp.referenceFilter     

#Filtered signal:  Direct Quantizer by Unifrom DAC 
u_direct_filter, error_direct, var_direct = sgp.signalFilter(u_direct)

#  Direct Quantizer by Non Unifrom DAC 
u_direct_INL_filter, error_INL_direct, var_INL_direct = sgp.signalFilter(u_direct_INL)

# Optimal Quantizer without INL feedback
u_mpc_filter, error_mpc, var_mpc = sgp.signalFilter(u_mpc)  # Quantized using unifrom DAC

# Optimal Quantizer for Unifrom DAC with INL feedback applied to Non-uniform DAC
u_mpc1_filter, error_mpc1, var_mpc1 = sgp.signalFilter(u_mpc1)  # Quantized using Non-unifrom DAC

# Optimal Quantizer with INL feedback
u_mpc_INL_filter, error_mpc_INL, var_mpc_INL = sgp.signalFilter(u_mpc_INL)  # Quantized using Non-unifrom DAC

# legend = ['Reference', 'Direct (Unifrom)', 'Direct(Non-uniform)', 'MPC(Unifrom)', 'MPC(Non-Uniform)', 'MPC(Non-Unifrom with  INL Feedback)']
# %%  Write data into file.
headerlist = ['Time', 'Reference', 'Direct (Unifrom)', 'Direct(Non-uniform)', 'MPC(Unifrom)', 'MPC(Non-Uniform)', 'MPC(Non-Unifrom with  INL Feedback)']
# headerlist = ['Time', 'Reference', 'Direct', 'Direct-INL', 'MPC', 'MPC-INL (w/o INL)',  'MPC with INL']
with open('simulationresult.csv','w') as f:
    writer = csv.writer(f, delimiter ='\t')
    writer.writerow(headerlist)
    writer.writerows(zip(t, filtered_reference, u_direct_filter, u_direct_INL_filter,  u_mpc_filter, u_mpc1_filter,  u_mpc_INL_filter))
# %% PLots
# plt.figure()
# plt.plot(t, filtered_reference)    
# plt.plot(t, u_direct_filter)  
# # plt.plot(t, u_direct_INL_filter)    
# # plt.plot(t, u_mhoq_filter)
# # plt.plot(t, u_mhoq_INL_filter)
# plt.plot(t, u_mpc_filter)
# # plt.plot(t, u_mpc1_filter)
# # plt.plot(t, u_mpc_INL_filter)
# plt.legend(leg)
# # plt.legend(['Reference', 'Direct Quantizer', 'MPC'])
# plt.xlabel('Time')
# plt.grid(True)


# # Plot of noise power
# bars = [var_direct, var_INL_direct, var_mpc, var_mpc1, var_mpc_INL] 
# # bars = [var_INL_direct, var_mpc1, var_mpc_INL] 
# x_pos = [0,1,2,3,4]  # x position of bars
# # bar plot noise power
# plt.figure()
# plt.bar(x_pos, bars, width = 0.9 )
# plt.xticks([i  for i in range(len(bars))],leg[1:len(leg)])
# for i in range(5):
#     plt.text(x = x_pos[i], y= bars[i] + 0.00015 , s= bars[i], size = 10)
# plt.subplots_adjust(bottom= 0.1, top = 1.5)
# plt.ylabel('Error Variance')
# plt.show()



# print(var_direct)
# print(var_mhoq)
