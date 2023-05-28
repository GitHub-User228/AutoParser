from parsers import Parser, ParserWithProxy
from F import save_as_csv, save_as_txt, gather_proxies, read_yaml, save_as_yaml, append_dict
import os

###########################################################################################
###                               Reading file with configs                             ###

dir_path = os.path.abspath(os.path.join(__file__ ,"../.."))
STORAGE_PATH = os.path.join(dir_path ,"data")
LOG_PATH = os.path.join(dir_path ,"log")
CONFIGS_PATH = os.path.join(dir_path ,"configs")

configs = read_yaml(path=CONFIGS_PATH,
                    filename='configs')

PARSER_CONFIGS = [dict(zip(configs['parser_config'].keys(),
                           [item[k] for item in configs['parser_config'].values()]))\
                  for k in range(len(list(configs['parser_config'].values())[0]))]


###########################################################################################
###                         Parsing urls with no proxy required                         ###

parser = Parser(waiting_time=configs['waiting_time']['no_proxy'],
                timeout_between_requests=configs['timeout_between_requests']['no_proxy'])

NO_PROXY_IDS = [it for it, item in enumerate(configs['source|url|requires_proxy']) if not item[2]]

data1, log_csv1, log_txt1 = parser.search(urls=[item[1] for it, item in enumerate(configs['source|url|requires_proxy']) if it in NO_PROXY_IDS],
                                       sources=[item[0] for it, item in enumerate(configs['source|url|requires_proxy']) if it in NO_PROXY_IDS],
                                       configs=[item for it, item in enumerate(PARSER_CONFIGS) if it in NO_PROXY_IDS],
                                       fields=configs['data_fields'],
                                       log_fields=configs['log_fields'],
                                       parser_types=[item for it, item in enumerate(configs['parser_type']) if it in NO_PROXY_IDS],
                                       number_of_tries=configs['number_of_tries']['no_proxy'])


###########################################################################################
###                                Saving data and log                                  ###

save_as_csv(file=log_csv1,
            path=LOG_PATH,
            filename=configs['log_filename']['no_proxy'])
save_as_txt(file=log_txt1,
            path=LOG_PATH,
            filename=configs['log_filename']['no_proxy'])
save_as_csv(file=data1,
            path=STORAGE_PATH,
            filename=configs['data_filename']['no_proxy'])


###########################################################################################
###                           Gathering a new set of proxies                            ###

old_proxies = read_yaml(path=CONFIGS_PATH,
                        filename='proxies')
new_proxies = gather_proxies()
proxies = append_dict(old_proxies, new_proxies)

PROXIES = [dict(zip(['http', 'https'], [item, item])) for item in proxies['items']]


###########################################################################################
###                           Parsing urls with proxy required                          ###

parser = ParserWithProxy(waiting_time=configs['waiting_time']['proxy'],
                         timeout_between_requests=configs['timeout_between_requests']['proxy'],
                         proxies=PROXIES)

PROXY_IDS = [it for it, item in enumerate(configs['source|url|requires_proxy']) if item[2]]

data2, log_csv2, log_txt2, proxies = \
                         parser.search(urls=[item[1] for it, item in enumerate(configs['source|url|requires_proxy']) if it in PROXY_IDS],
                                       sources=[item[0] for it, item in enumerate(configs['source|url|requires_proxy']) if it in PROXY_IDS],
                                       configs=[item for it, item in enumerate(PARSER_CONFIGS) if it in PROXY_IDS],
                                       fields=configs['data_fields'],
                                       log_fields=configs['log_fields'],
                                       parser_types=[item for it, item in enumerate(configs['parser_type']) if it in PROXY_IDS],
                                       number_of_tries=configs['number_of_tries']['proxy'])


###########################################################################################
###                   Saving data, log and successfully worked proxies                  ###

os.remove(f'{CONFIGS_PATH}/proxies.yaml')
save_as_yaml(file=proxies,
             path=CONFIGS_PATH,
             filename='proxies')

save_as_csv(file=log_csv2,
            path=LOG_PATH,
            filename=configs['log_filename']['proxy'])
save_as_txt(file=log_txt2,
            path=LOG_PATH,
            filename=configs['log_filename']['proxy'])
save_as_csv(file=data2,
            path=STORAGE_PATH,
            filename=configs['data_filename']['proxy'])