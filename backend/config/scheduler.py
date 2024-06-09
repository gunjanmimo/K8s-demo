from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import sys

# ---------------------------------LOCAL IMPORTS---------------------------------#
from background_tasks import check_image_processing_message_queue

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(
    scheduler, "interval", seconds=5, id="background_task", replace_existing=True
)
def background_task():
    check_image_processing_message_queue()


register_events(scheduler)


def start():
    scheduler.start()