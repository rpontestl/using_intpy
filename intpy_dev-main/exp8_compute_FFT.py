import time
import sys
import numpy as np
import numpy.random as rn

from intpy.intpy import initialize_intpy, deterministic


#deterministic não funciona devido a função rand
def compute_FFT(n):
    """
        Compute the FFT of an n-by-n matrix of data
    """
    matrix = rn.rand(n, n) + 1j * rn.randn(n, n)
    result = np.fft.fft2(matrix)
    result = np.abs(result)
    


@initialize_intpy(__file__)
def main(n):
    print(compute_FFT(n))


if __name__ == "__main__":
    n = int(sys.argv[1])
    start = time.perf_counter()
    main(n)
    print(time.perf_counter()-start)
