import feedparser
import datetime
import requests
import time
from bs4 import BeautifulSoup
import re


class BaseParser:
   """
   Base class for parsers

   Parameters
   ----------
   waiting_time : int or float
         Waiting time for response for request (in seconds)

   timeout_between_requests : int or float
         Time to wait between requests (in seconds)

   use_proxy : bool
         whether to use available proxies in proxies.yaml file
   """
   def __init__(self, waiting_time, timeout_between_requests, proxies=None):
      self.waiting_time = waiting_time
      self.timeout_between_requests = timeout_between_requests
      self.proxies = proxies

   def step(self, try_id, it, url, source, config, fields, log_fields, parser_type, kwargs={}):
      """
      Return parsed data and corresponding log for input url

      Parameters
      ----------
      it : int
          Index of input url in a set of urls to be parsed

      url : string
          Url to be parsed

      source : string
          Source name of url

      config : dict
          Dictionary with the configs for parser

      fields : array-like of strings
          Fields which are to be searched while parsing

      log_fields : array-like of strings
          Fields which are to be logged

      parser_type : string
          Type of parser to be used

      try_id : int
          try number

      kwargs : dict
          kwargs for request.get function

      Returns
      -------
      data : dict
          Dictionary with necessary fields retrieved from url
      log : dict
          Log of parsing process for specified url

      """
      data = dict(zip(fields, [[] for _ in range(len(fields))]))
      log = dict(zip(log_fields, [[''] for _ in range(len(log_fields))]))
      log['source'][0] = source
      log['TRY'][0] = f'{try_id+1}'

      try:
         response = requests.get(url, timeout=self.waiting_time, **kwargs)
         if f'{response.status_code}'[0] not in ['4', '5']:
            data, status_code = getattr(SubSteps, parser_type)(response, data, source, config)

            log['STATUS_CODE'][0] = status_code
            for key in [f for f in log_fields if f not in ['STATUS_CODE', 'ERROR', 'source', 'TRY']]:
               log[key][0] = str(len([1 for item in data[key] if item is not None]))

         else:
            log['STATUS_CODE'][0] = f'{(response.status_code)}'

      except Exception as e:
         log['ERROR'][0] = str(e)

      return data, log


   def search(self, urls, sources, configs, fields, log_fields, parser_types, number_of_tries):
      """
      Return parsed data and corresponding log for specified urls

      Parameters
      ----------
      urls : array-like of strings
          Set of urls to be parsed

      sources : array-like of strings
          Set of names of sources for urls

      configs : array-like of dicts
          Set with configs to be used for each url

      fields : array-like of strings
          Fields which are to be searched while parsing

      log_fields : array-like of strings
          Fields which are to be logged

      parser_types : array-like of strings
          types of parsers to be used for each url

      number_of_tries : int
          number of tries to be taken in order to parse successfully all urls

      Returns
      -------
      data : dict
          Dictionary with necessary fields retrieved from all urls
      log_csv : dict
          Log of parsing process of all urls (will be saved as csv)
      log_txt : list of strings
          Log of parsing process of all urls (will be saved as txt)
      """
      data = dict(zip(fields, [[] for _ in range(len(fields))]))
      log = dict(zip(log_fields, [[] for _ in range(len(log_fields))]))
      ids = [k for k in range(len(urls))]

      for try_id in range(number_of_tries):
         new_ids = []
         for it in ids:
            #print(f'{try_id+1} | {it} | {sources[it]}')
            data_, log_ = self.step(try_id, it, urls[it], sources[it], configs[it], fields, log_fields, parser_types[it])
            if log_['title'] in  [[''], ['0']]:
               new_ids.append(it)
            data = self.append(data, data_)
            log = self.append(log, log_)
            time.sleep(self.timeout_between_requests)
         if len(new_ids) == 0:
            break
         ids = new_ids

      log_txt = self.reform_log(log)
      log['TIME'] = [datetime.datetime.now() for _ in range(len(log[list(log.keys())[0]]))]
      log_csv = log
      return data, log_csv, log_txt

   @staticmethod
   def append(dict1, dict2):
      """
      Appends data2 dict to data1 dict

      Parameters
      ----------
      dict1 : dict
          Dictionary to which the data should be appended

      dict2 : dict
          Dictionary, data from which should be appended

      Returns
      -------
      dict1 : dict
          Dictionary with appended data
      """
      for key in dict1.keys():
         dict1[key] += dict2[key]

      return dict1

   @staticmethod
   def reform_log(log):
      """
      Reforms log to list of strings, which forms a table if is printed

      Parameters
      ----------
      log : dict
          Log of parsing process of all urls

      Returns
      -------
      out_log : list of strings
      """

      out_log = ['=' * 100,
                 f'TIME: {datetime.datetime.now()}']
      keys = list(log.keys())
      L1 = [len(str(key)) for key in log.keys()]
      L2 = [max([len(v) for v in values] + [0]) for values in log.values()]
      L = [max(l1, l2)+2 for (l1, l2) in zip(L1, L2)]

      separator = "+"+'+'.join(['-'*l for l in L]) + '+'
      out_log.append(separator)
      string = ''
      for j, key in enumerate(keys):
         spacing = (L[j] - L1[j]) // 2
         str_ = ' ' * spacing + f'{key}' + ' ' * spacing
         string = string + '|' + str_ + ' '*(L[j] - len(str_))
      string += '|'
      out_log.append(string)
      out_log.append(separator)
      for k in range(len(log[keys[0]])):
         string = ''
         for j, key in enumerate(keys):
            spacing = (L[j] - len(log[key][k]))//2
            str_ = ' '*spacing + f'{log[key][k]}' + ' '*spacing
            string = string + '|' + str_ + ' '*(L[j] - len(str_))
         string += '|'
         out_log.append(string)
         out_log.append(separator)
      out_log.append('')
      return out_log

###################################################################################################################

class Parser(BaseParser):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)

class ParserWithProxy(BaseParser):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)

   def search(self, urls, sources, configs, fields, log_fields, parser_types, number_of_tries):
      data = dict(zip(fields, [[] for _ in range(len(fields))]))
      log = dict(zip(['proxy_id','proxy']+log_fields, [[] for _ in range(len(['proxy_id','proxy']+log_fields))]))
      ids = [k for k in range(len(urls))]

      for proxy_id, proxy in enumerate(self.proxies):
         kwargs = {'proxies': proxy}
         for try_id in range(number_of_tries):
            new_ids = []
            for it in ids:
               #print(f'{proxy_id+1} | {try_id+1} | {it} | {sources[it]}')
               data_, log_ = self.step(try_id, it, urls[it], sources[it], configs[it], fields, log_fields, parser_types[it], kwargs)
               log_['proxy'] = [str(proxy['https'])]
               log_['proxy_id'] = [str(proxy_id+1)]
               if log_['title'] in  [[''], ['0']]:
                  new_ids.append(it)
               data = self.append(data, data_)
               log = self.append(log, log_)
               time.sleep(self.timeout_between_requests)
            if len(new_ids) == 0:
               break
            ids = new_ids
         if len(new_ids) == 0:
            break

      log_txt = self.reform_log(log)
      log['TIME'] = [datetime.datetime.now() for _ in range(len(log[list(log.keys())[0]]))]
      log_csv = log
      return data, log_csv, log_txt

###################################################################################################################

class SubSteps:
   @staticmethod
   def rss(response, data, source, config):
      """
      Parser of rss feeds
      """
      fp = feedparser.parse(response.text)
      status_code = str(response.status_code)
      for i in fp['entries']:
         data['title'].append(i[config['title_tag']])
         try:
            data['summary'].append(i[config['summary_tag']])
         except:
            data['summary'].append(None)
         date = i[config['date_tag']]
         data['date'].append(f'{date.tm_year}-{date.tm_mon}-{date.tm_mday}')
         data['link'].append(i[config['link_tag']])
         try:
            data['type'].append(i["tags"][0][config['type_tag']])
         except:
            data['type'].append(None)

      data['source'] = [source for _ in range(len(data['title']))]
      data['date_parsed'] = [datetime.datetime.now() for _ in range(len(data['title']))]

      return data, status_code

   @staticmethod
   def thebell(response, data, source, config=None):
      """
      Parser for TheBell
      """
      bs = BeautifulSoup(response.text, "lxml")
      status_code = str(response.status_code)

      texts = [str(k) for k in bs.find_all('div', class_=['line-widget ng-star-inserted'])]
      data['title'] = [BeautifulSoup(text).find('div', attrs={'class': re.compile(r"text text-33")}) for text in texts]
      data['summary'] = [None for text in texts]
      data['type'] = [BeautifulSoup(text).find('div', attrs={'class': re.compile(r"category category-33")}) for text in texts]
      data['date'] = [BeautifulSoup(text).find('div', attrs={'class': re.compile(r"time time-33")}) for text in texts]
      none_ids = [k for k in data['source'] if k is None]

      for key in ['title', 'summary', 'type', 'date']:
         data[key] = [item.text if item is not None else None for item in data[key]]
         data[key] = [item for k, item in enumerate(data[key]) if k not in none_ids]

      data['source'] = [source for _ in range(len(data['title']))]
      data['date_parsed'] = [datetime.datetime.now() for _ in range(len(data['title']))]

      return data, status_code