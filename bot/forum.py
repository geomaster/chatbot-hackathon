import requests
import json

def search(msg):
    s = requests.session()
    URL = 'https://forum.telenor.rs/api/core/v3/contents?filter=search(' + msg + ')'
    response = s.get(URL)
    log = open('log.txt', 'w')
    #jsonn = json.loads(response.text)
    #print()
    print(response.text.encode('utf-8'), file = log)
    exit(0)
    print(response.json())
    #print(json.dumps(jsonn, indent=2, ensure_ascii=False), file = log)
    return "2"

search('roming')