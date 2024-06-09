# --------------------------------DJANGO IMPORTS--------------------------------#
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import sys

# ---------------------------------LOCAL IMPORTS---------------------------------#
from background_tasks import check_image_processing_message_queue

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(
    scheduler, "interval", seconds=5, id="background_task", replace_existing=True
)
def background_task():
    """
    Background task that checks the image processing message queue at regular intervals.

    This function is scheduled to run every 5 seconds to ensure timely processing
    of image processing tasks. It calls the `check_image_processing_message_queue`
    function to pull and process messages from the Azure message queue.
    """
    check_image_processing_message_queue()


# Register scheduler events to ensure jobs are handled correctly
register_events(scheduler)


def start():
    """
    Starts the background scheduler to run the registered jobs.

    This function should be called to initiate the background scheduler
    and begin the periodic execution of scheduled tasks.
    """
    scheduler.start()
