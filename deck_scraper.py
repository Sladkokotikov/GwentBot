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

'''

'''
def smiles():
    sm = {}
    sm['Панцирь']= '''🦺'''
    sm['Сила природы'] = '''☠'''
    sm['Белый Хлад'] = '''❄'''
    sm['Стая главоглазов'] = '''🕷'''
    sm['Плоды Ийсгита'] = '''🪱'''
    sm['Запах крови'] = '''🧛'''
    sm['Неутолимый голод'] = '''🍖'''
    
    sm['Побуждение к действию']= '''⚡️'''
    sm['Королевское вдохновение'] = '''👑'''
    sm['Мобилизация'] = '''🚨'''
    sm['Стена щитов'] = '''🛡'''
    sm['Накопление'] = '''📈'''
    sm['Маневр'] = '''🧠'''
    sm['Ополчение'] = '''🔱'''
    
    sm['Партизанская тактика']= '''💣'''
    sm['Бодрость'] = '''😁'''
    sm['Дар природы'] = '''🌿'''
    sm['Точный удар'] = '''🏹'''
    sm['Засада ловчих'] = '''🧝‍♀️'''
    sm['Стремление к гармонии'] = '''☮'''
    sm['Махакамская кузня'] = '''⚒'''
    
    sm['Натиск']= '''🏴‍☠️'''
    sm['Безрассудная ярость'] = '''🔪'''
    sm['Боевой транс'] = '''🍄'''
    sm['Гнев моря'] = '''🌊'''
    sm['Ярость отцеубийцы'] = '''🪓'''
    sm['Медвежий ритуал'] = '''🐻'''
    sm['Пламя славы'] = '''💃'''
    
    sm['Заточение']= '''🚔'''
    sm['Имперское построение'] = '''🪖'''
    sm['Тактическое решение'] = '''👁‍🗨'''
    sm['Блокировка'] = '''🔒'''
    sm['Порабощение'] = '''⛓'''
    sm['Двойная игра'] = '''🎲'''
    sm['Самозванец'] = '''🎭'''
    
    sm['Кровавые деньги']= '''🤡'''
    sm['Джекпот'] = '''🤑'''
    sm['Богатей'] = '''💰'''
    sm['Теневая прибыль'] = '''💸'''
    sm['Священное братство'] = '''🔥'''
    sm['Пиратская бухта'] = '''⛵️'''
    sm['Тайник'] = '''🏦'''
    return sm
def get_golden(url):
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
        
        #print('{0} {1} {0}'.format(smiles()[ability],ability)) #ru[faction]
        #print(*golden, sep=', ')
        return '{0} {1} {0}'.format(smiles()[ability], ability)+'\n'+', '.join(golden)

