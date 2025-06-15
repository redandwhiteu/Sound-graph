import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.io import wavfile

def draw_waveform(file):
    sample_rate, data = wavfile.read(file)
    if len(data.shape) == 2:
        data = data[:, 0]

    data = data / np.max(np.abs(data))
    times = np.arange(len(data)) / sample_rate

    fig = plt.figure(figsize=(12, 6), dpi=300)  # 3600x1800 px
    plt.plot(times, data, linewidth=0.5, color='navy')
    plt.xlabel('Время [сек]')
    plt.ylabel('Амплитуда')
    plt.title(f'Звуковая волна {file}')
    plt.grid(True)
    plt.tight_layout()
    file_name = datetime.now().strftime('%Y%m%d-%H%M%S')
    plt.savefig(f'tmp/waveform_{file_name}.png', dpi=300)
    plt.close(fig)

    return f'tmp/waveform_{file_name}.png'