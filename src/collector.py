from parsers import Parser, ParserWithProxy
from transfer import save_as_csv, save_as_txt
import yaml
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(f"{dir_path}/configs.yaml", 'r') as f:
    configs = yaml.safe_load(f)

with open(f"{dir_path}/proxies.yaml", 'r') as f:
    proxies = yaml.safe_load(f)

PARSER_CONFIGS = [dict(zip(configs['parser_config'].keys(),
                           [item[k] for item in configs['parser_config'].values()]))\
                  for k in range(len(list(configs['parser_config'].values())[0]))]
PROXIES = [dict(zip(['http', 'https'], [item, item])) for item in proxies['items']]

### Parsing urls with no proxy required

parser = Parser(waiting_time=configs['waiting_time'],
                timeout_between_requests=configs['timeout_between_requests'])

NO_PROXY_IDS = [it for it, item in enumerate(configs['source|url|requires_proxy']) if not item[2]]

data1, log_csv1, log_txt1 = parser.search(urls=[item[1] for it, item in enumerate(configs['source|url|requires_proxy']) if it in NO_PROXY_IDS],
                                       sources=[item[0] for it, item in enumerate(configs['source|url|requires_proxy']) if it in NO_PROXY_IDS],
                                       configs=[item for it, item in enumerate(PARSER_CONFIGS) if it in NO_PROXY_IDS],
                                       fields=configs['data_fields'],
                                       log_fields=configs['log_fields'],
                                       parser_types=[item for it, item in enumerate(configs['parser_type']) if it in NO_PROXY_IDS],
                                       number_of_tries=configs['number_of_tries'])


### Parsing urls with proxy required

parser = ParserWithProxy(waiting_time=configs['waiting_time'],
                         timeout_between_requests=configs['timeout_between_requests'],
                         proxies=PROXIES)

PROXY_IDS = [it for it, item in enumerate(configs['source|url|requires_proxy']) if item[2]]

data2, log_csv2, log_txt2 = parser.search(urls=[item[1] for it, item in enumerate(configs['source|url|requires_proxy']) if it in PROXY_IDS],
                                       sources=[item[0] for it, item in enumerate(configs['source|url|requires_proxy']) if it in PROXY_IDS],
                                       configs=[item for it, item in enumerate(PARSER_CONFIGS) if it in PROXY_IDS],
                                       fields=configs['data_fields'],
                                       log_fields=configs['log_fields'],
                                       parser_types=[item for it, item in enumerate(configs['parser_type']) if it in PROXY_IDS],
                                       number_of_tries=configs['number_of_tries'])


### Saving data

save_as_csv(file=log_csv1,
            storage_path=configs['storage_path'],
            filename=configs['log_filename']['no_proxy'])
save_as_csv(file=log_csv2,
            storage_path=configs['storage_path'],
            filename=configs['log_filename']['proxy'])

save_as_txt(file=log_txt1,
            storage_path=configs['storage_path'],
            filename=configs['log_filename']['no_proxy'])
save_as_txt(file=log_txt2,
            storage_path=configs['storage_path'],
            filename=configs['log_filename']['proxy'])

save_as_csv(file=data1,
            storage_path=configs['storage_path'],
            filename=configs['data_filename']['no_proxy'])
save_as_csv(file=data2,
            storage_path=configs['storage_path'],
            filename=configs['data_filename']['proxy'])

