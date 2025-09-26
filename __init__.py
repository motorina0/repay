import asyncio

from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .crud import db
from .tasks import check_jobs_task, wait_for_paid_invoices
from .views import repay_generic_router
from .views_api import repay_api_router

repay_ext: APIRouter = APIRouter(prefix="/repay", tags=["RePay"])
repay_ext.include_router(repay_generic_router)
repay_ext.include_router(repay_api_router)


repay_static_files = [
    {
        "path": "/repay/static",
        "name": "repay_static",
    }
]

scheduled_tasks: list[asyncio.Task] = []


def repay_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def repay_start():
    task = create_permanent_unique_task("ext_repay", wait_for_paid_invoices)
    scheduled_tasks.append(task)
    task = create_permanent_unique_task("ext_repay_check_job", check_jobs_task)
    scheduled_tasks.append(task)


__all__ = [
    "db",
    "repay_ext",
    "repay_start",
    "repay_static_files",
    "repay_stop",
]
