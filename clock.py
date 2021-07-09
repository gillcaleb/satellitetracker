from apscheduler.schedulers.blocking import BlockingScheduler
from starlink_code import functions
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def background_update():
    functions.updateStarLink()

sched.start()
