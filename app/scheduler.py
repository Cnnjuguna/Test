import sched
import time
from tasks import update_next_donation_dates

# Creating a scheduler
scheduler = sched.scheduler(time.time, time.sleep)


# Defining the periodic task
def schedule_periodic_task(sc):
    update_next_donation_dates()
    sc.enter(
        86400, 1, schedule_periodic_task, (sc,)
    )  # Scheduling the task to run daily (86400 seconds)


# Scheduling the first run of the task
scheduler.enter(0, 1, schedule_periodic_task, (scheduler,))
scheduler.run()
