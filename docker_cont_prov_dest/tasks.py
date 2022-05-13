import time
from celery import shared_task, task

@shared_task
def send_mass_emails(recepient):
    print(recepient)
    print("started to sleep")
    time.sleep(5)
    print("wake up")
    return

@task
def send_scheduled_emails():
    pass