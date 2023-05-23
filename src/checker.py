import datetime

from crontab import CronTab

my_crons = CronTab(user='linuxuser')
for it, job in enumerate(my_crons):
    sch = job.schedule(date_from=datetime.datetime.now())
    print(f'{it+1} | Job: {job} | Next call: {sch.get_next()}')