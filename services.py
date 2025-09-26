from lnbits.core.models import Payment
from loguru import logger

from .crud import (
    create_extension_settings,  #
    get_extension_settings,  #
    update_extension_settings,  #
)
from .models import (
    ExtensionSettings,  #
)


async def payment_received_for_job_run(payment: Payment) -> bool:
    logger.info("Payment receive logic generation is disabled.")
    return True


async def get_settings(user_id: str) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, ExtensionSettings())
    return settings


async def update_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, data)
    else:
        settings = await update_extension_settings(user_id, data)

    return settings
