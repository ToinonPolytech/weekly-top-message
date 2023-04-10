from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='mon', hour=16,minute=12)
def scheduled_job():
    call(['python', 'main.py'])

scheduler.start()
