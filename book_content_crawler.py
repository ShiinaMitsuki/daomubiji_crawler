import os
import os.path as osp

import argparse
import pandas as pd
import tqdm
import requests

from lxml import etree

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def may_make_dir(path):
    assert path not in ['', None]

    if not osp.exists(path):
        os.makedirs(path)

    return path


def request_specific_content(url, xpath_patter):
    ctt = requests.get(url)
    ctt.encoding = 'utf-8'

    ctt.raise_for_status()

    html_obj = etree.HTML(ctt.text)

    return html_obj.xpath(xpath_patter)


def crawl_chapter(url, title):
    while True:
        try:
            raw_chapter_ctt = request_specific_content(url, r'//div[@class="content"]/p')
        except requests.HTTPError as error:
            print(error)
            continue

        valid_paragrahs = filter(lambda elm: len(elm.attrib) == 0 and elm.text is not None, raw_chapter_ctt)

        chapter_ctt = '\n\n'.join([ph.text for ph in valid_paragrahs])

        title = '\n\n=============================\n' \
                + '{}'.format(title).center(29, ' ') \
                + '\n=============================\n\n'

        break

    return title + chapter_ctt


def crawl_single_book(title, url):
    xpath_chapters = request_specific_content(url, r'//div[@class="panel"]/ul//a')

    # chapter_cnt = len(xpath_chapters)
    # print('book: {} has {} chapters...'.format(title, chapter_cnt))
    # print('crawling each chapters...')

    th_pool = ThreadPoolExecutor(num_thread)
    thread_handles = []

    with open(osp.join(may_make_dir(osp.join(dest, title)), '{}.txt'.format(title)), mode='wt') as fp:
        for idx, item in enumerate(xpath_chapters):
            chapter_url = item.get('href')
            chapter_title = item.text

            # chapter_content = crawl_chapter(chapter_url, chapter_title)
            thread_handles.append(th_pool.submit(crawl_chapter, chapter_url, chapter_title))

        for thh in tqdm.tqdm(thread_handles, desc=title, total=len(thread_handles), ncols=80):
            fp.write(thh.result())

    # th_pool.shutdown()

parser = argparse.ArgumentParser()
parser.add_argument('entry', type=str, metavar='PATH', help='path to book entries csv')
parser.add_argument('dst', type=str, metavar='PATh', help='save path')
parser.add_argument('--num_thread', type=int, default=8)
parser.add_argument('--num_process', type=int, default=0)

args = parser.parse_args()

entry_file = osp.expanduser(args.entry)
dest = may_make_dir(osp.expanduser(args.dst))
num_thread = args.num_thread
num_process = args.num_process

df = pd.read_csv(entry_file)

pr_pool = ProcessPoolExecutor(num_process)

if num_process == 0:
    for idx, row in df.iterrows():
        crawl_single_book(row['book'], row['entry'])
else:
    with ProcessPoolExecutor() as executor:
        for idx, row in df.iterrows():
            executor.submit(crawl_single_book, row['book'], row['entry'])
