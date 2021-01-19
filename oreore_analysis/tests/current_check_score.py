import requests

def current_score():
    r = requests.get("http://localhost:8888/current_score")
    print(r.json())
    # print(r.text)

if __name__ == "__main__":
    current_score()