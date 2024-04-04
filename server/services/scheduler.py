import threading
import asyncio
import main
from services.billing import issue_receipts_cron_job


# Schedule here the cron jobs to be executed


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


# Start a new event loop in a separate thread
new_loop = asyncio.new_event_loop()
t = threading.Thread(target=start_loop, args=(new_loop,))
t.start()


# Define a background task to run the scheduler
async def run_scheduler():
    while not main.shutdown_event.is_set():
        asyncio.run_coroutine_threadsafe(issue_receipts_cron_job(), new_loop)
        await asyncio.sleep(60)  # runs every minute
