"Pseudo-random generation"  
import math
import time as t
import re
import matplotlib.pyplot as plt
# N should refer to the number of numbers to generate
N = 40
def middle_square(seed = int((re.sub(r'\.(0*)', '', str(t.time())))[-6::])): 
    #The seed is biased and may not range all values
    ar = []
    for i in range(len(seed)):
        # x = len(str(seed))
        x = len(str(seed[i]))
        s = seed[i]**2
        while(len(str(s)) < 2*x): s*=10
        ar.append(int(str(s)[math.ceil(x*0.5):math.floor(x*1.5)]))
    return ar
def lehmer_gen(seed = int((re.sub(r'\.(0*)', '', str(t.time())))[-6::])):
    ar = []
    r = 10
    a = 7**5
    m = 2**31-1 
    for i in range(len(seed)):
        for j in range(r):
            seed[j] = a*seed[j]%m
        ar.append(seed[j])
    return ar


