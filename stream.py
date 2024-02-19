import array as arr
from time import time
import statistics
import sys 
import matplotlib.pyplot as plt
import numpy as np

#--------------------------------- Array initialisation ---------------------


def get_test_arrays(array_size):
    # Initializing Python lists
    a1 = [1.0 for i in range(array_size)]
    b1 = [2.0 for i in range(array_size)]
    c1 = [0.0 for i in range(array_size)]

    # Initializing arrays
    a2 = arr.array('d', a1)
    b2 = arr.array('d', b1)
    c2 = arr.array('d', c1)
    
    scalar = 2.0
    
    return [a1, b1, c1, a2, b2, c2, scalar]





#------------------------------------ Timing the operations -----------------------------------------
# Function for running the benchmark
def run_STREAM_average(a, b, c, scalar, array_size, n):
    
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
        
    for t in range(4):
        times[t] = statistics.mean(times[t])
    
    return times


def get_memory_bandwidths(array_size, times_list, times_array):
    def get_estimated_array_size(a):
        return 8 * array_size

    def get_ops_data_moved(a):
        size = sys.getsizeof(a)
        return (2 * size, 3 * size, 2 * size, 3 * size)

    def get_bandwidths(ops_data_moved, times):
        bandwidths = []
        for i in range(4):
            bandwidths.append(ops_data_moved[i] / times[i])

        return bandwidths

    data_moved_list = get_ops_data_moved(a1)
    data_moved_array = get_ops_data_moved(a2)

    return (get_bandwidths(data_moved_list, times_list), get_bandwidths(data_moved_array, times_array))

#---------------- combined -------------
array_sizes_to_test = [10 ** i for i in range(1,5)] + [10 ** 6 * i for i in range(2, 6)]

results_list = []
results_array = []

counter = 1
test_number = len(array_sizes_to_test)

for size in array_sizes_to_test:
    print("Running test " + str(counter) + " out of " + str(test_number))
    a1, b1, c1, a2, b2, c2, scalar = get_test_arrays(size)
    times_list = run_STREAM_average(a1, b1, c1, scalar, size, 100)
    times_array = run_STREAM_average(a2, b2, c2, scalar, size, 100)
    
    memory_bandwidths_list, memory_bandwidths_array = get_memory_bandwidths(size, times_list, times_array)
    
    results_list.append(memory_bandwidths_list)
    results_array.append(memory_bandwidths_array)
    counter += 1
    
print("Done")


# ------------------- Plotting results -----------


def get_points_xy(operation_id, array_sizes, results):
    points = []

    for i in range(len(array_sizes)):
        points.append([array_sizes[i], results[i][operation_id]])
    
        
    data = np.array([points])
    x, y = data.T
    
    x = np.log10(x)
    
    return [x, y]
    
    
def plot_operation(operation_id, results, color, label):
    x, y = get_points_xy(operation_id, array_sizes_to_test, results)
    plt.scatter(x, y, color=color, marker='o', label=label)

plot_operation(0, results_list, 'red', 'copy list')
plot_operation(0, results_array, 'green', 'copy array')
plt.legend(['COPY with lists','COPY with arrays']) 
plt.title("COPY Comparison")
plt.xlabel('STREAM_ARRAY_SIZE (log10 scale)')
plt.ylabel('Memory bandwith in B/s (linear scale)')
plt.show()


plot_operation(1, results_list, 'red', 'add list')
plot_operation(1, results_array, 'green', 'add array')
plt.legend(['COPY with lists','COPY with arrays']) 
plt.title("ADD Comparison")
plt.xlabel('STREAM_ARRAY_SIZE (log10 scale)')
plt.ylabel('Memory bandwith in B/s (linear scale)')
plt.show()


plot_operation(2, results_list, 'red', 'add list')
plot_operation(2, results_array, 'green', 'add array')
plt.legend(['SCALE with lists','SCALE with arrays']) 
plt.title("SCALE Comparison")
plt.xlabel('STREAM_ARRAY_SIZE (log10 scale)')
plt.ylabel('Memory bandwith (linear scale)')
plt.show()


plot_operation(3, results_list, 'red', 'add list')
plot_operation(3, results_array, 'green', 'add array')
plt.legend(['TRIAD with lists','TRIAD with arrays']) 
plt.title("TRIAD Comparison")
plt.xlabel('STREAM_ARRAY_SIZE (log10 scale)')
plt.ylabel('Memory bandwith in B/s (linear scale)')
plt.show()
