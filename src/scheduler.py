from crontab import CronTab
import os
from F import read_yaml

###########################################################################################
###                               Reading file with configs                             ###

dir_path = os.path.abspath(os.path.join(__file__ ,"../.."))
LOG_PATH = os.path.join(dir_path ,"log")
SRC_PATH = os.path.join(dir_path ,"src")
CONFIGS_PATH = os.path.join(dir_path ,"configs")

configs = read_yaml(path=CONFIGS_PATH,
                    filename='configs')


###########################################################################################
###                               Accessing Cron Jobs                                   ###

my_cron = CronTab(user=configs['username'])


###########################################################################################
###                            Deleting all existing jobs                               ###

for job in my_cron:
    my_cron.remove(job)


###########################################################################################
###                                Defining new job                                     ###

job = my_cron.new(command=f'python3 {SRC_PATH}/collector.py >> {LOG_PATH}/output.txt')
job.setall(configs['schedule'])
my_cron.write()

for job in my_cron:
    print(job)


