from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone

from chat.models import Message

@periodic_task(run_every=crontab(minute='*/5'))
def delete_old_messages():
    # Query all the foos in our database
    msgs = Message.objects.all()

    # Iterate through them
    for msg in msgs:

        # If the expiration date is bigger than now delete it
        if msg.expiration < timezone.now():
            msg.delete()
            # log deletion
    return "completed deleting msgs at {}".format(timezone.now())
