from pydub import AudioSegment
from time import sleep


# timeで指定した分だけ、音声をスライスする処理。　eg: 10000=10秒
def extracting_from_last(time=10000, import_file="./example.wav", export_file="./output.wav"):
    time = -time
    sound = AudioSegment.from_file(import_file, format="wav")
    sliced_sound = sound[time:]
    sliced_sound.export(export_file, format="wav")
    print("completed slice!")

def loop_extract_loop():
    sleep_time = 10
    import_file = "/var/spool/asterisk/monitor/record-in.wav" 
    while True:
        extracting_from_last(import_file=import_file)
        sleep(sleep_time)

if __name__ == "__main__":
    # extracting_from_last()
    loop_extract_loop()
