import datetime
from crontab import CronTab
import os
from F import read_yaml

###########################################################################################
###                               Reading file with configs                             ###

dir_path = os.path.abspath(os.path.join(__file__ ,"../.."))
CONFIGS_PATH = os.path.join(dir_path ,"configs")

configs = read_yaml(path=CONFIGS_PATH,
                    filename='configs')

###########################################################################################
###                  Outputting the time of a next call of parsing job                  ###

for it, job in enumerate(CronTab(user=configs['username'])):
    sch = job.schedule(date_from=datetime.datetime.now())
    print(f'{it+1} | Job: {job} | Next call: {sch.get_next()}')