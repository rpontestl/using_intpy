
#!/usr/bin/env python

import time
import numpy as np
import sys

from intpy.intpy import initialize_intpy, deterministic


#---------------------------
# Function: raised_to_string
#---------------------------
def raised_to_string(x):
    """
        Convert to int, then raise the input to the power of itself.
    """
    x = int(x)
    if x == 0:
        return 0
    else:
        return x**x

#--------------------
# Function: raised_to
#--------------------
def raised_to(x):
    """
        Raise the input to the power of itself
    """
    if x == 0:
        return 0
    else:
        return x**x

power_of_digits = [raised_to(i) for i in range(10)]

#-------------------------------
# Function: is_munchausen_number
#-------------------------------
def is_munchausen_number(i):
    return i == sum(power_of_digits[int(x)] for x in str(i))

#----------------------------------
# Function: find_munchausen_numbers
#----------------------------------
@deterministic
def find_munchausen_numbers(x):
    """
        Find the 4 Munchausen numbers
    """
    number = 0
    i = 0
    while True:
        if is_munchausen_number(i):
            number += 1
            print("Munchausen number %d: %d" % (number, i))

        if (number == 4):
            break

        i += 1

#--------------------------------------
# Function: find_munchausen_numbers_map
#--------------------------------------
def find_munchausen_numbers_map():
    """
        Find the 4 Munchausen numbers using map()
    """
    num = 0
    i = 0
    while True:
        if i == sum(map(raised_to_string, str(i))):
            num += 1
            print("Munchausen number %d: %d" %(num, i))
        if (num == 4):
            break
        i += 1


@initialize_intpy(__file__)
def main(): 
    print(find_munchausen_numbers(0))


if __name__ == "__main__":
    n = int(sys.argv[1])
    start = time.perf_counter()
    main()
    print(time.perf_counter()-start)
