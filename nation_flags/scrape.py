import requests
from lxml import html
import json
import re
from settings import config
import urllib2
import time

def get_english_content():
    return requests.get(config['ENGLISH_URL'])

def get_japanese_content():
    return requests.get(config['JAPANESE_URL'])

def get_dom_tree(content):
    return html.fromstring(content)

def get_english_dom_tree():
    return get_dom_tree(get_english_content().content)

def get_japanese_dom_tree():
    return get_dom_tree(get_japanese_content().content)

def get_nation_name(img_src):
    return img_src.attrib['alt'][8:].strip()

def get_flag_url(img_src):
    return img_src.attrib['src']

def get_flag(flag_url):
    flag = re.search('/(?P<flag>Flag_of.*svg)/', flag_url).group('flag')
    flag = flag.replace("_%28converted%29", "")
    flag = flag.replace("_%28civil%29", "")
    flag = flag.replace("_%28state%29", "")
    flag = flag.replace("_%28Pantone%29", "")
    if flag == 'Flag_of_Transnistria.svg':
        flag = 'Flag_of_Transnistria_%28state%29.svg'
    return flag

def get_nation_name_j(j_tree, flag):
    img_src_j = j_tree.xpath('//img[contains(@src, "{}")]'.format(flag))
    return img_src_j[0].attrib['alt'][:-2].encode('utf-8')

def get_wikipedia_url(nation_name_e):
    nation_name_e = nation_name_e.replace("the ", "", 1).replace(" ", "_")
    return "{}{}".format(config['WIKIPEDIA_BASE_URL'], nation_name_e)

def get_wikipedia_url_j(nation_name_j):
    return "{}{}".format(config['WIKIPEDIA_BASE_URL_J'], urllib2.quote(nation_name_j))

def get_nations():
    e_tree = get_english_dom_tree()
    j_tree = get_japanese_dom_tree()

    nations = []
    for img_src in e_tree.xpath('//*[@id="mw-content-text"]//td/a/img'):
        nation_name = get_nation_name(img_src)
        flag_url = get_flag_url(img_src)
        flag = get_flag(flag_url)
        nation_name_j = get_nation_name_j(j_tree, flag)
        nations.append({
            "nation_name_e": nation_name,
            "png_url": "http:{}".format(flag_url),
            "nation_name_j": nation_name_j,
            "wikipedia_url": get_wikipedia_url(nation_name),
            "wikipedia_url_j": get_wikipedia_url_j(nation_name_j)
        })
    return nations

if __name__ == '__main__':
    for nation in get_nations():
        try:
            urllib2.urlopen(nation['png_url'])
        except Exception, e:
            print(str(e), nation['png_url'])
        time.sleep(1)

        try:
            urllib2.urlopen(nation['wikipedia_url'])
        except Exception, e:
            print(str(e), nation['wikipedia_url'])
        time.sleep(1)

        try:
            urllib2.urlopen(nation['wikipedia_url_j'])
        except Exception, e:
            print(str(e), nation['wikipedia_url_j'])
        time.sleep(1)
