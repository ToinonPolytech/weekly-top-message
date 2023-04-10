from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='mon', hour=15,minute=15)
def scheduled_job():
    call(['python', 'main.py'])

scheduler.start()
