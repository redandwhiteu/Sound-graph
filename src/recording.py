import pyaudio
import wave

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

    wf = wave.open('tmp/sound.wav', 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()