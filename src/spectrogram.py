import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.signal import spectrogram
from scipy.io import wavfile


def draw_spectrogram(file):
    sample_rate, data = wavfile.read(file)
    if len(data.shape) == 2:
        data = data[:, 0]

    f, t, Sxx = spectrogram(data, fs=sample_rate)
    fig = plt.figure(figsize=(12, 6), dpi=300)
    plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='magma')
    plt.ylabel('Частота [Гц]')
    plt.xlabel('Время [сек]')
    plt.title(f'Спектрограмма {file}')
    plt.colorbar(label='dB')
    plt.tight_layout()
    file_name = datetime.now().strftime('%Y%m%d-%H%M%S')
    plt.savefig(f'tmp/spectrogram_{file_name}.png', dpi=300)
    plt.close(fig)

    return f'tmp/spectrogram_{file_name}.png'