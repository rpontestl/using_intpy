#!/usr/bin/env python

import time
import numpy as np
import sys

from intpy.intpy import initialize_intpy, deterministic


integrand = lambda x: np.exp(x)

@deterministic
def compute_quadrature(n):
    """
      Perform the Gauss-Legendre Quadrature at the prescribed order n
    """
    a = -3.0
    b = 3.0

    # Gauss-Legendre (default interval is [-1, 1])
    x, w = np.polynomial.legendre.leggauss(n)

    # Translate x values from the interval [-1, 1] to [a, b]
    t = 0.5*(x + 1)*(b - a) + a

    gauss = sum(w * integrand(t)) * 0.5*(b - a)


@initialize_intpy(__file__)
def main(n):
    print('Gauss-Legendre Quadrature of order: ', n)
    print(compute_quadrature(n))


if __name__ == "__main__":
    n = int(sys.argv[1])
    start = time.perf_counter()
    main(n)
    print(time.perf_counter()-start)
