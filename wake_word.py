import pvporcupine
import pyaudio
import struct

def detect_wake_word(keyword="zarn", callback=None):
    porcupine = pvporcupine.create(keywords=[keyword])
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    try:
        print("Listening for wake word...")
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                print("Wake word detected!")
                if callback:
                    callback()
    except KeyboardInterrupt:
        print("Exiting wake word detection.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
