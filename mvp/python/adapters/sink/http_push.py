import json, urllib.request

class HttpSink:
    def __init__(self, cfg):
        self.url = cfg['url']
    def send(self, payload: dict):
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.url, data=data, headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status
