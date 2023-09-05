# Direct Quantizer
import numpy as np
from scipy import linalg

# Perfrom the quatnization of the input signal
# Q _ quantizer set or the quantization levels
# ref - input/reference signal
# Returns the quantized values of the refernce signal (ref)

def DirectQuantization(Q, ref):
    u_d = []
    for k in range(0, len(ref)):
        e_n = []
        for i in Q:
            err = linalg.norm(ref[k]-i)
            e_n.append(err)
        
        min_err = np.min(e_n)
        ind = e_n.index(min_err)
        u_directi = Q[ind]
        u_d.append(u_directi)
    return u_d 