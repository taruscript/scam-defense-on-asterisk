from pydub import AudioSegment
from time import sleep
import requests
from scipy.io import wavfile
from pydub.utils import mediainfo
import shutil
import os


# timeで指定した分だけ、音声をスライスする処理。　eg: 10000=10秒
def extracting_from_last(time=20000, import_file="./example.wav", export_file="./output.wav"):
    os.system(f'ffmpeg -y -i "{import_file}" -ar 44100 "output2.wav"')
    time = -time
    sound = AudioSegment.from_file("output2.wav", format="wav")
    sliced_sound = sound[time:]
    sliced_sound.export("output2.wav", format="wav")
    print("completed slice!")

    # current_time = float(mediainfo(import_file)["duration"])
    # trimming_calc = current_time - time
    # sampleRate, waveData = wavfile.read(import_file)
    # startSample = int(trimming_calc  * sampleRate )
    # endSample = int( current_time * sampleRate )
    # wavfile.write( export_file, sampleRate, waveData[startSample:endSample])
    # print("completed slice!")



# def trim_wav(originalWavPath, newWavPath , start, end ):

 
 
# wp = r"pathToWav.wav"
# trim_wav(wp, wp.replace(".wav", "_trimmed.wav"), 0,10)


# スライス済みの音声ファイルをpostし特殊詐欺を解析する。
def post_wav_extracted():
    fileName = './output2.wav'
    files = {'file': open(fileName, 'rb')}
    r = requests.post("http://localhost:8888/scam_check", files=files)
    print(r.json())  

# 10秒録音して、10秒待機するという処理を永遠に繰り返す
def loop_extract_loop():
    sleep_time = 5
    import_file = "/var/spool/asterisk/monitor/record-in.wav" 
    while True:
        shutil.copyfile(import_file, "./output.wav")
        extracting_from_last(import_file="./output.wav")
        post_wav_extracted()
        sleep(sleep_time)
  

if __name__ == "__main__":
    # extracting_from_last()
    loop_extract_loop()
