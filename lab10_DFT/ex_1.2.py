import numpy as np

def DFT(vector):
    n = vector.shape[0]
    j=np.arange(n)
    k = np.arange(n)
    j = k.reshape((n,1))
    Fn = np.exp(-2j * np.pi * j * k / n)
    return Fn.dot(vector)

vector = np.random.random(20)
print("DFT from implementation")
print(DFT(vector).flatten(), end="\n\n")

print("DFT from library")
print(np.fft.fft(vector).flatten())