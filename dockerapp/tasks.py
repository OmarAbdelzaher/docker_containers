import time
from celery import shared_task, task

@shared_task
def create_container(container_data):
    print(container_data,"create")

@shared_task
def destroy_container(container_data):
    print(container_data,"destroy")
    
# for scheduled tasks
@task
def send_scheduled_emails():
    pass