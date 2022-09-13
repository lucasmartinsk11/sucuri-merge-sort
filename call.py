import sys
import requests

def call(m):
    request = requests.get("http://127.0.0.1:5000/"+str(m))
    print(request.content)


def callALot(n, m):

    for i in range(0, n):
        call(m)

callALot(int(sys.argv[1]), int(sys.argv[2]))
