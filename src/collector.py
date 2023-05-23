from parsers import RSSParser
from transfer import save_as_csv, save_as_txt
import yaml

with open("configs.yaml", 'r') as f:
    configs = yaml.safe_load(f)

PARSER_CONFIGS = [dict(zip(configs['parser_config'].keys(),
                           [item[k] for item in configs['parser_config'].values()]))\
                  for k in range(len(list(configs['parser_config'].values())[0]))]


parser = RSSParser(waiting_time=configs['waiting_time'],
                   timeout_between_requests=configs['timeout_between_requests'])

data, log_csv, log_txt = parser.search(urls=[item[1] for item in configs['source|url']],
                                       sources=[item[0] for item in configs['source|url']],
                                       configs=PARSER_CONFIGS,
                                       fields=configs['data_fields'],
                                       log_fields=configs['log_fields'])

save_as_csv(file=log_csv,
            storage_path=configs['storage_path'],
            filename=configs['log_filename'])

save_as_txt(file=log_txt,
            storage_path=configs['storage_path'],
            filename=configs['log_filename'])

save_as_csv(file=data,
            storage_path=configs['storage_path'],
            filename=configs['data_filename'])




