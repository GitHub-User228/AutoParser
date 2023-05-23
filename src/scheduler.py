from crontab import CronTab
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

my_cron = CronTab(user='linuxuser')

for job in my_cron:
    my_cron.remove(job)

job = my_cron.new(command=f'python3 {dir_path}/collector.py')
job.setall('0 * * * *')
my_cron.write()

for job in my_cron:
    print(job)


