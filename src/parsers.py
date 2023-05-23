import feedparser
import datetime
import requests
import time


class BaseParser():
   """
   Base class for parsers

   Parameters
   ----------
   waiting_time : int or float
         Waiting time for response for request (in seconds)

   timeout_between_requests : int or float
         Time to wait between requests (in seconds
   """
   def __init__(self, waiting_time, timeout_between_requests):
      self.waiting_time = waiting_time
      self.timeout_between_requests = timeout_between_requests

   def step(self, it, url, source, config, fields, log_fields):
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

      Returns
      -------
      data : dict
          Dictionary with necessary fields retrieved from url
      log : dict
          Log of parsing process for specified url

      """
      data = dict(zip(fields, [[] for _ in range(len(fields))]))
      log = dict(zip(fields, [[] for _ in range(len(log_fields))]))

      return data, log


   def search(self, urls, sources, configs, fields, log_fields):
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

      for it, url in enumerate(urls):
         data_, log_ = self.step(it, url, sources[it], configs[it], fields, log_fields)
         data = self.append(data, data_)
         log = self.append(log, log_)
         time.sleep(self.timeout_between_requests)

      log_txt = self.reform_log(log)
      log['TIME'] = [datetime.datetime.now() for _ in range(len(urls))]
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


class RSSParser(BaseParser):
   """
   Class for parsing RSS feeds
   """
   def __init__(self, **kwargs):
      super().__init__(**kwargs)

   def step(self, it, url, source, config, fields, log_fields):
      data = dict(zip(fields, [[] for _ in range(len(fields))]))
      log = dict(zip(log_fields, [[''] for _ in range(len(log_fields))]))

      log['source'][0] = source

      try:
         response = requests.get(url, timeout=self.waiting_time)
         if f'{response.status_code}'[0] not in ['4', '5']:
            fp = feedparser.parse(url)
            log['STATUS_CODE'][0] = str(fp['status'])
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
            for key in [f for f in log_fields if f not in ['STATUS_CODE', 'ERROR', 'source']]:
               log[key][0] = str(len([1 for item in data[key] if item is not None]))

         else:
            log['STATUS_CODE'][0] = f'{(response.status_code)}'

      except Exception as e:
         log['ERROR'][0] = str(e)

      return data, log


