import numpy as np
import matplotlib.pyplot as plt

def save_diagram(freq, values, title):
    mask = freq > 0
    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax1.plot(freq[mask], values[mask])
    ax1.set_title(title)
    fig.savefig(title + '.png')

x = np.linspace(0, 100, 1000)
omg = 2 * np.pi
sig1 = np.sin(omg * 1 * x)
sig2 = np.sin(omg * 2 * x)
sig3 = np.sin(omg * 4 * x)
signal1 = np.fft.fft(sig1 + sig2 + sig3)
freq = np.fft.fftfreq(x.size, 0.1)
fourier_real = omg * (signal1 / 1000).real
fourier_imag = omg * (signal1 / 1000).imag

save_diagram(freq, fourier_real, "a_real")
save_diagram(freq, fourier_imag, "a_imag")

sig1_sliced = sig1[0:334]
sig2_sliced = sig2[334:667]
sig3_sliced = sig3[667:1000]

signal2 = np.fft.fft(np.concatenate((sig1_sliced, sig2_sliced, sig3_sliced), axis=None))
fourier_real = omg * (signal2 / 1000).real
fourier_imag = omg * (signal2 / 1000).imag

save_diagram(freq, fourier_real, "b_real")
save_diagram(freq, fourier_imag, "b_imag")