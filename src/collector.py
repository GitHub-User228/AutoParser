from parsers import RSSParser
from transfer import save_as_csv, save_as_txt

STORAGE_PATH = "/home/linuxuser/AutoParser/data"
FILENAME = "raw_data"
LOG_FILENAME = 'log'

URLS = ["https://ria.ru/export/rss2/archive/index.xml",
        'https://tass.ru/rss/v2.xml']

SOURCES = ['ria',
           'tass']

DEFAULT_CONFIG = {'title_tag': 'title',
                  'summary_tag': 'summary',
                  'date_tag': 'published_parsed',
                  'link_tag': 'link',
                  'type_tag': 'term'}

CONFIGS = [DEFAULT_CONFIG for _ in range(len(URLS))]

FIELDS = ['title', 'summary', 'date', 'link', 'type', 'source', 'date_parsed']
LOG_FILEDS = ['source', 'STATUS_CODE', 'ERROR', 'title', 'summary', 'date', 'link', 'type']

parser = RSSParser()
data, log_csv, log_txt = parser.search(urls=URLS,
                                       sources=SOURCES,
                                       configs=CONFIGS,
                                       fields=FIELDS,
                                       log_fields=LOG_FILEDS)

save_as_csv(file=log_csv,
            storage_path=STORAGE_PATH,
            filename=LOG_FILENAME)

save_as_txt(file=log_txt,
            storage_path=STORAGE_PATH,
            filename=LOG_FILENAME)

save_as_csv(file=data,
            storage_path=STORAGE_PATH,
            filename=FILENAME)




