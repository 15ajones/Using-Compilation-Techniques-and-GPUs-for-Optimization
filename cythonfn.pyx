from time import time
def run_STREAM_average_array(double[:]a, double[:]b, double[:]c, double scalar, int array_size, int n):
    cdef int i, j
    times = [[] for i in range(4)]
    
    for i in range(n):
        # COPY
        times[0].append(time())
        for j in range(len(a)):
            c[j] = a[j]
        times[0][-1] = time() - times[0][-1]

        # ADD
        times[2].append(time())
        for j in range(len(a)):
             c[j] = a[j]+b[j]
        times[2][-1] = time() - times[2][-1]

        # SCALE
        times[1].append(time())
        for j in range(len(a)):
             b[j] = scalar*c[j]
        times[1][-1] = time() - times[1][-1]

        # TRIAD
        times[3].append(time())
        for j in range(len(a)):
            a[j] = b[j]+scalar*c[j]
        times[3][-1] = time() - times[3][-1]
        
    return times