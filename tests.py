import requests
import threading


class Req(threading.Thread):
    def __init__(self):
        super(Req, self).__init__()
        print("Start_thread")

    def run(self):
        r = requests.get('http://127.0.0.1:9090')
        print(r.content)


q = []
for i in range(1000):
    w = Req()
    w.setDaemon(True)
    w.start()
    q.append(w)
for t in q:
    t.join()
