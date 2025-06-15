import pyaudio
import wave

from datetime import datetime


def recording(index, seconds):
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 2,
                    rate = 44100,
                    frames_per_buffer = 1024,
                    input_device_index = index,
                    input = True)

    frames = []
    for i in range(0, int((44100 / 1024) * int(seconds))):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    file_name = datetime.now().strftime('%Y%m%d-%H%M%S')
    wf = wave.open(f'tmp/record_{file_name}.wav', 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    return f'tmp/record_{file_name}.wav'