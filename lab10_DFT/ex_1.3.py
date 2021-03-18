import numpy as np

def DFT(vector):
    n = vector.shape[0]
    Fn = create_Fn(n)
    return Fn.dot(vector)

def create_Fn(n):
    j = np.arange(n)
    k = np.arange(n)
    j = k.reshape((n, 1))
    Fn = np.exp(-2j * np.pi * j * k / n)
    return Fn

vector = np.random.random(20)
n = vector.shape[0]
Fn = create_Fn(n)
result = np.conj(Fn.dot(np.conj(DFT(vector)))) / n

print("Original vector")
print(vector, end="\n\n")

print("IDFT from implementation")
print(result.flatten(), end="\n\n")

print("IDFT from library")
print(np.fft.ifft(np.fft.fft(vector)).flatten())