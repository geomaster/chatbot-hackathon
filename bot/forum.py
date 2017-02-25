import requests
import json
import html2text

def search(msg):
    s = requests.session()
    URL = 'https://forum.telenor.rs/api/core/v3/contents?filter=search(' + msg + ')'
    response = s.get(URL)
    
    #log = open('log.txt', 'w')
    #log_info = open('log_info.txt', 'w')

    text = response.text#.encode('utf-8')
    if text[0] != '{':
        lines = text.split('\n')
        text = ''.join(lines[1:])

    
    obj = json.loads(text)
    #print(json.dumps(obj, indent=4, sort_keys=True), file = log)

    if len(obj['list']) == 0:
        return None

    info = []

    best = dict()
    fb = True
    parent_place = ''

    for x in obj['list']:
        m = dict()
        m['subject'] = x['subject']
        if fb:
            best['subject'] = x['subject']
        if 'favoriteObject' in x and 'content' in x['favoriteObject']:
            m['content'] = x['favoriteObject']['content']
            if fb:
                best['content'] = x['favoriteObject']['content']
                #if 'parentPlace' in x:
                #    parent_place = x['parentPlace']['html']
                fb = False
        elif 'question' in x and x['question'] == False:
            m['content'] = x['content']
            if fb:
                best['content'] = x['content']
                #if 'parentPlace' in x:
                #    parent_place = x['parentPlace']['html']
                fb = False
        else:
            m['content'] = 'BURAZ NE ZNAM JSON'
        info.append(m)

    #print(json.dumps(info, indent=4, sort_keys=True), file = log_info)

    h = html2text.HTML2Text()
    h.ignore_links = True

    if 'content' not in best:
        return None
    text_response = h.handle(best['content']['text'])
    pair = dict()

    text_response.strip()

    text_response = text_response[:300].strip() + '...'

    #if parent_place != '':
    #    text_response += 'Vise o tome: ' + parent_place


    pair['a'] = text_response
    pair['q'] = best['subject']
    return pair

