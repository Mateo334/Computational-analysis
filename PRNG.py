"Pseudo-random generation"  
import math
import time as t
import re
import matplotlib.pyplot as plt
# N should refer to the number of numbers to generate
N = 40
def seed_gen():
    """Generates the starting seed. Not to be purely 
    probabilistic to test the stochasticity of each generator."""
    return int((re.sub(r'\.(0*)', '', str(t.time())))[-8::])
def middle_square(number_of_values, *order_of_value):
    """Returns a list of random integers using the middle-square method.""" 
    ar = []
    iters = 10
    for i in range(number_of_values):
        seed = seed_gen()
        for j in range(iters):
            seed = seed**2
            s = str(seed)
            ln = len(str(s))
            if(len(s)%2 or len(s)<= 2*order_of_value):#The number is odd, add zeros
                s = s.zfill(2*order_of_value)
                ln = len(str(s))
            seed = int(s[(ln-order_of_value)//2:(ln+order_of_value)//2])
        ar.append(seed)
    return ar

def iterative_gens(number_of_values, which_gen = 0, *order_of_value):
    """Returns a list of random integers using the iterative generators. Has multiple modes."""
    ar = []
    gens = ["LCG",  "blum_blum_shub","Lehmer"]
    iters = 50
    if(which_gen==0):
        m, a, c = 2**32, 214013, 2531011  
        gen_func = lambda seed: (a*seed+c)%m
    elif(which_gen==1):
        p = 383
        q = 1000033
        M = p*q
        gen_func = lambda seed: (seed**2)%M
    elif(which_gen==2):
        a = 7**5
        m = 2**31-1 
        gen_func = lambda seed: a*seed%m

        
    for i in range(number_of_values):
        seed = seed_gen()
        for j in range(iters):
            seed = gen_func(seed)
        ar.append(seed)
    return ar


print(iterative_gens(10, 1))