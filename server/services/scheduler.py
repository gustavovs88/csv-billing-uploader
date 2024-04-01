import schedule
import asyncio
import main
from services.billing import issue_pending_receipts_in_thread


# Schedule here the cron jobs to be executed
schedule.every().hours.do(issue_pending_receipts_in_thread)


# Define a background task to run the scheduler
async def run_scheduler():
    while not main.shutdown_event.is_set():
        schedule.run_pending()
        await asyncio.sleep(60)
