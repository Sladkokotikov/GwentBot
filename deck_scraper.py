from urllib.request import urlopen, unquote
import re
from itertools import product

def get_tag(page, tag):
    return list(set(re.findall('"{0}":"?(.+?)(?=")'.format(tag), page)))

def where(dic, pred):
    ans = {}
    for key in dic:
        if pred(dic[key]):
            ans[key] = dic[key]
    return ans

def faction_w_smiles(faction):
    if faction == "skellige":
        return '''🌊''' + " Скеллиге"
    if faction == "monsters":
        return '''👹''' + " Чудовища"
    if faction == "nilfgaard":
        return '''🌞''' + " Нильфгаард"
    if faction == "scoiatael":
        return '''🐿''' + " Скоя'таэли"
    if faction == "syndicate":
        return '''💰''' + " Синдикат"
    if faction == "northernrealms":
        return '''⚜️''' + " Королевства Севера"
    return faction

def get_golden(url):

    with open("custom_log.txt", 'a') as log:
        log.write(url + '\n')
    
    with urlopen(url) as page:
        s = page.read().decode('utf-8').replace('&quot;', '"')
        nums = list(product('0123456789abcdef', repeat=4))
        nums = list(map(lambda x: ''.join(x), nums))
        d = {}
        for n in nums:
            d[n] = chr(int(n, base=16))
        s = re.sub('\\\\u[0-9a-f]{4}', lambda x: d[x.group()[2:]], s)
        s = s.replace('&#039;', "'")
        s = s.split('slotImgCn')
        s1 = s[1]
        #print(s1)
        ability = get_tag(s1, 'localizedName')[0]
        faction = get_tag(s1, 'slug')[0]
        t = s[2:]
        cards = {}
        for c in t:
            try:
                name = get_tag(c, 'localizedName')[0]
                prov = get_tag(c, 'provisionsCost')[0].strip(',')
                rary = get_tag(c, 'rarity')[0]
                cards[name] = rary, prov
            except:
                pass
        cards.pop(ability)
        golden = where(cards, lambda x: x[0][0] in 'le')
        golden = list(dict(sorted(golden.items(), key = lambda x: int(x[1][1]), reverse=True)).keys())
        
        stratagem = list(where(cards, lambda x: x[1]=='0').keys())[0]
        golden.remove(stratagem)
        if stratagem not in ['Волшебная лампа', 'Тактическое преимущество']:
            golden.insert(0, stratagem)
        message = ""
        message += faction_w_smiles(faction) + ' - ' + ability
        message += '\n'
        message += ', '.join(golden)
        return message
