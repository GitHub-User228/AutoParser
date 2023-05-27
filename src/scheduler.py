from crontab import CronTab
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

my_cron = CronTab(user='linuxuser')

for job in my_cron:
    my_cron.remove(job)

job = my_cron.new(command=f'python3 {dir_path}/collector.py >> {dir_path}/out.txt  2>&1')
#job.setall('* 0,3,6,9,12,15,18,21 * * *')
job.setall('0 0,2,4,6,8,10,12,14,16,18,20,22 * * *')
#job.setall('38 * * * *')
my_cron.write()

for job in my_cron:
    print(job)


