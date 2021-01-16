import requests

def put_wav():
    fileName = './output.wav'
    files = {'file': open(fileName, 'rb')}
    r = requests.post("http://localhost:8888/scam_check", files=files)
    print(r.json())
    # print(r.text)

if __name__ == "__main__":
    put_wav()