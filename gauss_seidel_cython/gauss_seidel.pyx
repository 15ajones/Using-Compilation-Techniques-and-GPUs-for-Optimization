import numpy as np
cimport numpy as np

def gauss_seidel(np.ndarray[np.double_t, ndim=2] f):
    newf: double[:,:] = f.copy()
    
    cdef unsigned int i, j
    
    for i in range(1, newf.shape[0]-1):
        for j in range(1, newf.shape[1]-1):
            newf[i,j] = 0.25 * (newf[i,j+1] + newf[i,j-1] + newf[i+1,j] + newf[i-1,j])  
    
    return newf

