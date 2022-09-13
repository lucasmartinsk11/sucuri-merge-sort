import sys
import requests

def call():
    request = requests.get("http://127.0.0.1:5000/")
    print(request.content)


def callALot(n):

    for i in range(0, n):
        call()

callALot(int(sys.argv[1]))
