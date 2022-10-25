import time
import sys
import numpy as np
import numpy.random as rn

from intpy.intpy import initialize_intpy, deterministic

def loop_time_step(u):
    """
        Take a time step in the desired numerical solution 
        u found using loops
    """
    n, m = u.shape

    error = 0.0
    for i in range(1, n-1):
        for j in range(1, m-1):
            temp = u[i, j]
            u[i, j] = (
                       (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])*4.0 +
                       u[i-1, j-1] + u[i-1, j+1] + u[i+1, j-1] +
                       u[i+1, j+1]
            )/20.0

            difference = u[i, j] - temp
            error += difference*difference

    return u, np.sqrt(error)

def vector_time_step(u):
    """
        Take a time step in the desired numerical solution v 
        found using vectorization
    """
    u_old = u.copy()
    u[1:-1, 1:-1] = (
                     (u[0:-2, 1:-1] + u[2:, 1:-1] + u[1:-1, 0:-2] +
                      u[1:-1, 2:])*4.0 +
                     u[0:-2, 0:-2] + u[0:-2, 2:] + u[2:, 0:-2] + u[2:, 2:]
    )/20.0

    return u, np.linalg.norm(u-u_old)

@deterministic
def loop_solver(n):
    """
        Find the desired numerical solution using loops
    """

    j = complex(0, 1)
    pi_c = np.pi

    # Set the initial condition
    u = np.zeros((n, n), dtype=float)

    #       Set the boundary condition
    x = np.r_[0.0:pi_c:n*j]
    u[0, :] = np.sin(x)
    u[n-1, :] = np.sin(x)*np.exp(-pi_c)

    iteration = 0
    error = 2
    while(iteration < 100000 and error > 1e-6):
        (u, error) = loop_time_step(u)
        iteration += 1
    return (u, error, iteration)

@deterministic
def vectorized_solver(n):
    """
        Find the desired numerical solution using vectorization
    """
    j = complex(0, 1)
    pi_c = np.pi

    # Set the initial condition
    u = np.zeros((n, n), dtype=float)

    # Set the boundary condition
    x = np.r_[0.0:pi_c:n*j]
    u[0, :] = np.sin(x)
    u[n-1, :] = np.sin(x)*np.exp(-pi_c)

    iteration = 0
    error = 2
    while(iteration < 100000 and error > 1e-6):
        (u, error) = vector_time_step(u)
        iteration += 1
    return (u, error, iteration)
    

@initialize_intpy(__file__)
def main(n):
    start = time.perf_counter()
    print(loop_solver(n))
    print('loop solver time: '+ (str) (time.perf_counter()-start)+' s')
    start = time.perf_counter()
    print(vectorized_solver(n))
    print('vectorized solver time: '+(str) (time.perf_counter()-start)+ ' s')

if __name__ == "__main__":
    n = int(sys.argv[1])
    main(n)
    
