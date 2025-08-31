from PRNG import *
#For checking the stochasticity of the PRNGs


def time_sampling(N):
    """Samples pseudo-random seeds of up to 1e6 based on time."""
    x = []
    for i in range(N):
        num = int((re.sub(r'\.(0*)', '', str(t.time())))[-6::])
        while(num<10**5):
            num = int((re.sub(r'\.(0*)', '', str(t.time())))[-6::]) #6 means up to 10**6
        # Here you can modify the range
        x.append(num)
        t.sleep(1e-10)
    return x



N = 100
def plotter(N, f):
    """Plots the data wrt time sampled seed of number N and function f."""
    x = time_sampling(N)
    plt.scatter([i for i in range(N)], [f(a) for a in x])
    plt.show()
plotter(N, middle_square)

def birthday_spacings(data):
    """checks the distance between the points. May fit it to an exponential."""
    data = sorted(data)
    dists = []
    for i in range(0, len(data)-1):
        dists.append(abs(data[i]-data[i+1]))
    dists = sorted(dists)[::-1]
    plt.scatter([i for i in range(len(dists))], dists)
    plt.show()
# birthday_spacings(lehmer_gen(time_sampling(N)))    
# birthday_spacings(middle_square(time_sampling(N)))    