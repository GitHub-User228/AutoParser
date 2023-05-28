import csv
import yaml
from proxy_parse import ProxyParser
import os
from pathlib import Path

def save_as_txt(file, path, filename):
    with open(f'{path}/{filename}.txt', 'a') as f:
        for item in file:
            f.write(f'{item}\n')


def save_as_csv(file, path, filename):
    f = Path(f'{path}/{filename}.csv')
    if f.is_file():
        with open(f'{path}/{filename}.csv', 'a', encoding='utf8', newline='') as a:
            w = csv.writer(a)
            if os.stat(f'{path}/{filename}.csv').st_size == 0:
                w.writerow(file.keys())
            w.writerows(zip(*file.values()))
    else:
        with open(f'{path}/{filename}.csv', 'a', encoding='utf8', newline='') as a:
            w = csv.writer(a)
            w.writerow(file.keys())
            w.writerows(zip(*file.values()))


def read_yaml(path, filename):
    with open(f"{path}/{filename}.yaml", 'r') as f:
        file = yaml.safe_load(f)
    return file


def save_as_yaml(file, path, filename):
    with open(f'{path}/{filename}.yaml', 'a') as w:
        yaml.dump(file, w, default_flow_style=False)


def gather_proxies():
    """
    Gathering available proxies using ProxyParser library

    Returns
    -------
    proxies : dict
        Dictionary with proxies in format d['items'] = list of proxies
    """
    proxy_parser = ProxyParser()
    proxies_list = proxy_parser.parse()
    proxies = {}
    proxies['items'] = [k for k in proxies_list if ('https' in k)]
    return proxies


def append_dict(dict1, dict2):
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