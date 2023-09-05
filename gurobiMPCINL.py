"""
Created on Mon Aug  7 13:20:51 2023

@author: bikashadhikari
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np
# import matplotlib.pyplot as plt
# from scipy import signal
# from my_functions import direct_quantizer
# import statistics
# %%
# import DirectQantization as dq

# class gurobiMPCINL:
    
def add_INL(u_opt, Q, INL):
     rem = u_opt - int(u_opt)
     if rem <= 0.5:
         u_opt = np.floor(u_opt)
     else:
         u_opt = np.ceil(u_opt)

     u_op_INL = 0
     INL_dict = dict(zip(Q, INL))
     INL_i = INL_dict[u_opt]
     u_op_INL = u_opt + INL_i
     return u_op_INL

def MPC(x0, N, ref, A, B, C, D, t, Q, INL):
     # INPUTS:
     # x0 - initial state
     # N - prediction horizon
     # ref - reference input signal
     # A, B, C, D - state space matrix of low pass filter
     # t - total simulation time

     len_ref = len(t)
     u_mpc = []
     j = 0
     # MPC Uniform
     # xx = []
     while j <= len_ref:
         m = gp.Model("MPC")
         u = m.addMVar(N, vtype=GRB.INTEGER, name= "u", lb = np.min(Q), ub = np.max(Q))  # control variable
         x = m.addMVar((2*(N+1), 1), vtype= GRB.CONTINUOUS, lb= -GRB.INFINITY, ub = GRB.INFINITY, name = "x") # state variable

         # Objective function
         obj = 0                  # initialize objective function
         for i in range(0, N):
             k = 2*i
             con = u[i]-ref[j+i]
             e_t = C @ x[k:k+2] + D*con
             obj = obj + e_t*e_t
    
         # Constraint Set
         # cons = [] # initialize constraint set
         m.addConstr(x[0:2, :] == x0)  # initial condition constraint
    
         for i in range(0, N):
             k = 2*i
             st = x[k:k+2]
             con = u[i]-ref[j + i]  # current control
             f_value = A @ st + B * con  # function value
             st_next = x[k+2: k+4]
             m.addConstr(st_next == f_value)
    
         m.update
         m.setObjective(obj, GRB.MINIMIZE)
         # m.params.MIPFocus= 1 #  find feasible solutions quickly
         # m.params.MIPFocus= 2 # if there is not difficulty in finding the feasible solution but we want to focus
                                 # on providing the optimiality of the solutions
         #m.params.MIPFocus= 3 # if you want your run to imporve the best objective bound
#         m.tune
         # 1: show the log in console ; 0: does not show the log in console
         m.Params.LogToConsole = 0
         m.optimize()  # optimize
    
         allvars = m.getVars()
         values = m.getAttr("X", allvars)
         values = np.array(values)
    
         control_u = values[0:N]  # optimal control variables
         states_x = values[N:len(values)]  # optimal state variavles
    
         # Store the first value of the optimal quantizer
         u_opt = control_u[0]  # moving horizon control
         # u_mpc = np.append(u_mpc, u_opt)  # store the optimal value
         u_opt = add_INL(u_opt, Q, INL)
         u_mpc = np.append(u_mpc, u_opt)  # store the optimal value
    
         # apply the new optimal control to the system
         x0_new = A @ x0 + B*(u_opt - ref[j])
         # this updates states is the new initial condition for the next prediction horizon
         # set the new initial condition as the prediction using optimal control.
         x0 = x0_new
         j += 1
     return u_mpc

        
