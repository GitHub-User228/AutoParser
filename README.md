# AutoParser
Here you can find an example of how to automate parsing process of news rss feeds
(or any news sites with certain modifications) using Cron Jobs and (optionally) proxies, which are also dynamically parsed


## Libraries used
- feedparser
- bs4
- proxy_parse
- crontab

## Folders & Files description
- [configs](configs) folder - contains yaml files with configs and proxies
   - [configs.yaml](configs/configs.yaml) - configs to be used
   - [proxies.yaml](configs/proxies.yaml) - proxies to be used (dynamically changing)
- [data](data) folder - contains parsed data in csv format (separately for proxy and no proxy cases)
   - [raw_data.csv](data/raw_data.csv) - dataset for urls with no proxy required while parsing
   - [raw_data_proxy.csv](data/raw_data_proxy.csv) - dataset for urls with proxy required while parsing
- [log](log) folder - contains log in txt and csv format (separately for proxy and no proxy cases)
   - [log.csv](log/log.csv) - log for urls with no proxy required while parsing
   - [log.txt](log/log.txt) - log for urls with no proxy required while parsing
   - [log_proxy.csv](log/log_proxy.csv) - log for urls with proxy required while parsing
   - [log_proxy.txt](log/log_proxy.txt) - log for urls with proxy required while parsing
- [src](src) folder - contains python code
   - [checker.py](src/checker.py) - checks the time when the next call of a job will be made
   - [scheduler.py](src/scheduler.py) - schedules parsing job (and deleting previous jobs)
   - [parsers.py](src/parsers.py) - contains parsers classes
   - [F.py](src/F.py) - contains loading and saving functions, ``gather_proxies`` method used to collect available proxies
   - [collector.py](src/collector.py) - function used to parse news data from specified urls when called

## How to use it?
1. Modify [configs.yaml](configs/configs.yaml)
    - ``username`` - username of your environment
    - ``schedule`` - schedule to be used by Cron Jobs for parsing job
    - ``data_filename`` - names of files with parsed data (proxy & no proxy)
    - ``log_filename`` - names of files with log (proxy & no proxy)
    - ``timeout_between_requests`` - time (in seconds) to wait between sequential requests (proxy & no proxy)
    - ``waiting_time`` - time (in seconds) to wait for response from site (proxy & no proxy)
    - ``number_of_tries`` - number of attempts to take in case of failed request (proxy & no proxy)
    - ``parser_type`` - parser type to be used for specified urls (rss or custom)
    - ``parser_config`` - tags to be used for urls with rss feeds (None otherwise)
    - ``source|url|requires_proxy`` - source name, corresponding url and whether a proxy must be used
2. Modify [parsers.py](src/parsers.py)
    - create new custom method inside ``SubSteps`` class if there are urls with custom parser required
3. Run commands
    - ``sudo service cron stop`` - stop all jobs
    - ``python3 scheduler.py`` - schedule parsing job (and deleting previous jobs)
    - ``sudo service cron start`` - start parsing job
    - ``python3 checker.py`` - check the time when the next call will be made

PS: run ``python3 collector.py`` in case you need to perform parsing manually
