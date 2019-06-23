- Requirements

```
python >= 3.6

requests
lxml
pandas
tqdm
```

```shell
pip install -r requirements.txt
```
- Run

1. gather book entries

```shell
python book_entry_crawler.py
```

2. choose the books you want to keep by editing the csv

3. crawl each book

```shell
python book_content_crawler.py <path_to_the_csv_file> <path_to_the_save_dir>
```

4. enjoy a cup of coffe