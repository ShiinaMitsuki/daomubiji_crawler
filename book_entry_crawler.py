import requests
import pandas as pd

from lxml import etree


entry_url = r'http://www.daomubiji.org/'

ctt = requests.get(entry_url)
ctt.encoding = 'utf-8'

ctt.raise_for_status()

patter = r'//div[@class="header"]/center/a'

html_obj = etree.HTML(ctt.text)

xpath_book_entries = html_obj.xpath(patter)

print('we got {} book entries'.format(len(xpath_book_entries)))

books, entries = [], []

for xp in xpath_book_entries:
    title = xp.text
    href = xp.get('href')
    print('book: {} entry: {}'.format(title, href))

    books.append(title)
    entries.append(href)

df = pd.DataFrame(dict(
    book=books,
    entry=entries
))

df.to_csv('save/book_entries.csv')