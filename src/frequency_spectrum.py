import os

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.io import wavfile


def draw_frequency_spectrum(file):
    sample_rate, data = wavfile.read(file)
    if len(data.shape) == 2:
        data = data[:, 0]

    N = len(data)
    fft_data = np.fft.fft(data)
    fft_freq = np.fft.fftfreq(N, d=1/sample_rate)

    mask = fft_freq >= 0
    frequencies = fft_freq[mask]
    amplitudes = np.abs(fft_data[mask])

    fig = plt.figure(figsize=(12, 6), dpi=300)

    plt.plot(frequencies, amplitudes, color='darkred')
    plt.xlabel('Частота [Гц]')
    plt.ylabel('Амплитуда')
    plt.title(f'Частотный спектр {file}')
    plt.grid(True)

    file_name = datetime.now().strftime('%Y%m%d-%H%M%S')
    plt.tight_layout()
    plt.savefig(f'tmp/freq_spectrum_{file_name}.png', dpi=300)
    plt.close(fig)

    return f'tmp/freq_spectrum_{file_name}.png'