import numpy as np
from timeit import default_timer as timer
import gauss_seidel

grid_sizes = [10 * i for i in range(25)]

n_experiments = 2

results = []

for s in grid_sizes:
    print("Grid size: ", s)
    times = np.zeros((n_experiments))
    for i in range(n_experiments):
        print("Experiment: ", i)
        f = np.zeros((s, s))
        f[1:-1, 1:-1] = 1
        
        start = timer()
        for j in range(1000):
            f = gauss_seidel.gauss_seidel(f)
        end = timer()
        
        times[i] = end - start
    
    results.append(np.mean(times))
    print(results[-1])

    np.save("out.npy", results)

test = np.load("out.npy")
print(test)
