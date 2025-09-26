import asyncio
from datetime import datetime

from lnbits.core.models import Payment
from lnbits.tasks import register_invoice_listener
from loguru import logger

from .crud import get_all_enabled_job_configs
from .services import payment_received_for_job_run

#######################################
########## RUN YOUR TASKS HERE ########
#######################################

# The usual task is to listen to invoices related to this extension


async def wait_for_paid_invoices():
    invoice_queue = asyncio.Queue()
    register_invoice_listener(invoice_queue, "ext_repay")
    while True:
        payment = await invoice_queue.get()
        await on_invoice_paid(payment)


# Do somethhing when an invoice related top this extension is paid


async def on_invoice_paid(payment: Payment) -> None:
    if payment.extra.get("tag") != "repay":
        return

    logger.info(f"Invoice paid for repay: {payment.payment_hash}")

    try:
        await payment_received_for_job_run(payment)
    except Exception as e:
        logger.error(f"Error processing payment for repay: {e}")


async def check_jobs_task() -> None:
    print("### check_jobs_task 1000")
    while True:
        print("### check_jobs_task 1001")
        job_configs = await get_all_enabled_job_configs()
        now = datetime.now()
        print("### check_jobs_task job_configs 1002", len(job_configs), now)
        for job_config in job_configs:
            if job_config.match_cron(now):
                print(f"### Running job: {job_config.name}", now)

        await asyncio.sleep(10)

    print("### check_jobs_task END")
