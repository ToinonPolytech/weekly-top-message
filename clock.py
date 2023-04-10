from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='mon', hour=9)
def scheduled_job():
    call(['python', 'NOM_DE_VOTRE_SCRIPT.py'])

scheduler.start()
