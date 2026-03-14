import pvporcupine
from pvrecorder import PvRecorder

porcupine = pvporcupine.create(
  access_key=' .', #access key
  keyword_paths=[r"C:\Users\aru06\OneDrive\Desktop\codes\HACKATHONS\AIandDataScience4good\Roh-help_en_windows_v4_0_0\Roh-help_en_windows_v4_0_0.ppn"]
)

recorder = PvRecorder(frame_length=porcupine.frame_length)
recorder.start()

def get_next_audio_frame():
    return recorder.read()

try:
    while True:
        audio_frame = get_next_audio_frame()
        keyword_index = porcupine.process(audio_frame)

        if keyword_index >= 0:
            print("Roh-help detected")

finally:
    recorder.stop()
    recorder.delete()
    porcupine.delete()
