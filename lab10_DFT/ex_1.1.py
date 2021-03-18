import numpy as np
import time

def DFT(vector):
    n = vector.shape[0]
    j=np.arange(n)
    k = np.arange(n)
    j = k.reshape((n,1))
    Fn = np.exp(-2j * np.pi * j * k / n)
    return Fn.dot(vector)

def CT(vector):
    n = vector.shape[0]

    if (n % 2 > 0):
        raise ValueError("not even")
    elif (n <= 8):
        return DFT(vector)
    else:
        vector_even = CT(vector[::2])
        vector_odd = CT(vector[1::2])

        fac = np.exp( -2j * np.pi * np.arange(n) / n)
        return np.concatenate([vector_even + fac[:n//2] * vector_odd,
                               vector_even + fac[n//2:] * vector_odd])


vector = np.random.random(4096)
start = time.time()
res1 = DFT(vector)
end = time.time()
print(f"Slow DFT - time: {end-start}")
print(res1.flatten(), end='\n\n')

start = time.time()
res2 = CT(vector)
end = time.time()
print(f"Cooley-Turkey - time: {end-start}")
print(res2.flatten(), end='\n\n')

start = time.time()
res3 = np.fft.fft(vector)
end = time.time()
print(f"Library function - time: {end-start}")
print(res3.flatten())
