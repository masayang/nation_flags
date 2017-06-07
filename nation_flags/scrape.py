import requests
from lxml import html
import json

english_content = requests.get(
    'https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags'
)

japanese_content = requests.get(
    'https://ja.wikipedia.org/wiki/%E5%9B%BD%E6%97%97%E3%81%AE%E4%B8%80%E8%A6%A7'
)

e_tree = html.fromstring(english_content.content)
j_tree = html.fromstring(japanese_content.content)

img_srcs = e_tree.xpath('//*[@id="mw-content-text"]//td/a/img')
for img_src in img_srcs:
    nation_name = img_src.attrib['alt'][8:]
    flag_url = img_src.attrib['src']
    print(json.dumps({
        "nation_name_e": nation_name,
        "png_url": flag_url
    }, indent=4, sort_keys=True))


