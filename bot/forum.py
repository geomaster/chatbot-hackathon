import requests
import json
import html2text

def search(msg):
    s = requests.session()
    URL = 'https://forum.telenor.rs/api/core/v3/contents?filter=search(' + msg + ')'
    response = s.get(URL)
    log = open('log.txt', 'w')

    log_info = open('log_info.txt', 'w')

    text = response.text#.encode('utf-8')
    if text[0] != '{':
        lines = text.split('\n')
        text = ''.join(lines[1:])

    print(text, file = log)
    obj = json.loads(text)

    if len(obj['list']) == 0:
        return None

    info = []

    for x in obj['list']:
        m = dict()
        m['subject'] = x['subject']
        m['content'] = x['content']
        info.append(m)


    print(info, file = log_info)

    h = html2text.HTML2Text()
    h.ignore_links = True

    text_response = h.handle(info[0]['content']['text'])
    pair = dict()
    pair['a'] = text_response
    pair['q'] = info[0]['subject']
    return pair
