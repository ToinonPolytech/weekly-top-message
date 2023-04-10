from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='mon', hour=17,minute=01)
def scheduled_job():
    call(['python', 'main.py'])

scheduler.start()
