
'''

TINY_GSGP.py: A Tiny and Efficient Implementation of Geometric Semantic Genetic Programming Using Higher-Order Functions and Memoization

Author: Alberto Moraglio (albmor@gmail.com) 

Features:

- Individuals are represented directly as Python (anonymous) functions.

- Crossover and mutation are higher-order functions.

- Offspring functions call parent functions rather than embed their definitions (no grwoth, implicit ancestry trace).

- Memoization of individuals turns time complexity of fitness evalutation from exponential to constant.

- The final solution is a compiled function. It can be extracted using the ancestry trace to reconstruct its 'source code'. 

This implementation is to evolve Boolean expressions. It can be easily adapted to evolve arithmetic expressions or classifiers.

'''

import random
import itertools
import time

from functools import cmp_to_key

#from intpy.intpy import initialize_intpy, deterministic
from intpy.intpy import deterministic

#### PARAMETERS ####

NUMVARS = 5 # number of input variables
DEPTH = 4 # maximum depth of expressions in the initial population
POPSIZE = 20 # population size
GENERATIONS = 15 # number of generations
TRUNC = 0.5 # proportion of population to retain in truncation selection

####################

vars = ['x'+str(i) for i in range(NUMVARS)] # variable names

def memoize(f):
    'Add a cache memory to the input function.'
    f.cache = {}
    def decorated_function(*args):
        if args in f.cache:
            return f.cache[args]
        else:
            f.cache[args] = f(*args)
            return f.cache[args]
    return decorated_function

def randexpr(dep):
    'Create a random Boolean expression.'
    if dep==1 or random.random()<1.0/(2**dep-1):
        return random.choice(vars)
    if random.random()<1.0/3:
        return 'not' + ' ' + randexpr(dep-1) 
    else:
        return '(' + randexpr(dep-1) + ' ' + random.choice(['and','or']) + ' ' + randexpr(dep-1) + ')'


def randfunct():
    'Create a random Boolean function. Individuals are represented _directly_ as Python functions.'
    re = randexpr(DEPTH)
    rf = eval('lambda ' + ', '.join(vars) + ': ' + re) # create function of n input variables
    #rf = memoize(rf) # add cache to the function
    rf.geno = lambda: re # store genotype
    return rf

def targetfunct(*args):
    'Parity function of any number of input variables'
    return args.count(True) % 2 == 1

def fitness(individual):
    'Determine the fitness (error) of an individual. Lower is better.'
    fit = 0
    somelists = [[True,False] for i in range(NUMVARS)]
    for element in itertools.product(*somelists): # generate all input combinations for n variables
        if individual(*element) != targetfunct(*element):
            fit = fit + 1
    return fit

@deterministic
def crossover(p1,p2):
    """
    The crossover operator is a higher order function that takes parent functions and return an offspring function.
    The definitions of parent functions are _not substituted_ in the definition of the offspring function.
    Instead parent functions are _called_ from the offspring function. This prevents exponential growth.    
    """
    mask = randfunct()
    offspring = lambda *x: (p1(*x) and mask(*x)) or (p2(*x) and not mask(*x))
    #offspring = memoize(offspring) # add cache
    offspring.geno = lambda: '(('+ p1.geno() + ' and ' + mask.geno() + ') or (' + p2.geno() + ' and not ' + mask.geno() + '))' # to reconstruct genotype
    return offspring

#@deterministic
def mutation(p):
    'The mutation operator is a higher order function. The parent function is called by the offspring function.'
    mintermexpr = ' and '.join([random.choice([x,'not ' + x]) for x in vars]) # random minterm expression of n variables
    minterm = eval('lambda ' + ', '.join(vars) + ': ' + mintermexpr) # turn minterm into a function
    if random.random()<0.5:
        offspring = lambda *x: p(*x) or minterm(*x)
        #offspring = memoize(offspring) # add cache
        offspring.geno = lambda: '(' + p.geno() + ' or ' + mintermexpr + ')' # to reconstruct genotype
    else:
        offspring = lambda *x: p(*x) and not minterm(*x)
        #offspring = memoize(offspring) # add cache
        offspring.geno = lambda: '(' + p.geno() + ' and not ' + mintermexpr + ')' # to reconstruct genotype
    return offspring

#@initialize_intpy(__file__)
def main():
    'Main function.'
    #pop = [ randfunct() for _ in xrange(POPSIZE) ] # initialise population
    pop = [ randfunct() for _ in range(POPSIZE) ] # 4py3
    #print(pop)

    def cmp(a,b):
        try:
            return (a > b) - (a < b)
        except TypeError:
            s1, s2 = type(a).__name__, type(b).__name__
            return (s1 > s2) - (s1 < s2)

    #for gen in xrange(GENERATIONS+1):
    for gen in range(GENERATIONS+1): # 4py3
        graded_pop = [ (fitness(ind), ind) for ind in pop ] # evaluate population fitness
        #print(graded_pop)
        sgp = sorted(graded_pop, key=cmp_to_key(cmp))
        #print(sgp)
        #sorted_pop = [ ind[1] for ind in sorted(graded_pop)] # sort population on fitness
        sorted_pop = [ ind[1] for ind in sgp] # sort population on fitness
        #print 'gen: ', gen , ' min fit: ', fitness(sorted_pop[0]), ' avg fit: ', sum(ind[0] for ind in graded_pop)/(POPSIZE*1.0) # print stats
        print('gen: ', gen , ' min fit: ', fitness(sorted_pop[0]), ' avg fit: ', sum(ind[0] for ind in graded_pop)/(POPSIZE*1.0)) # 4py3
        parent_pop = sorted_pop[:int(TRUNC*POPSIZE)] # selected parents
        if gen == GENERATIONS: break
        #for i in xrange(POPSIZE): # create offspring population
        for i in range(POPSIZE): # create offspring population    
            par = random.sample(parent_pop, 2) # pick two random parents
            pop[i] = mutation(crossover(par[0],par[1])) # create offspring

    #print 'Best individual in last population: '
    print('Best individual in last population: ') # 4py3
    #print (sorted_pop[0]).geno() # reconstruct genotype of final solution (WARNING: EXPONENTIALLY LONG IN NUMBER OF GENERATIONS!)
    #print 'Query best individual in last population with all True inputs:'
    print('Query best individual in last population with all True inputs:') # 4py3
    #print sorted_pop[0](*([True] * NUMVARS)) # however querying it to make predictions is quick
    print(sorted_pop[0](*([True] * NUMVARS))) # 4py3

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(time.perf_counter()-start)
