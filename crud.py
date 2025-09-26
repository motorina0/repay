# Description: This file contains the CRUD operations for talking to the database.


from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import (
    CreateJobConfig,
    CreateJobRun,
    ExtensionSettings,  #
    JobConfig,
    JobConfigFilters,
    JobRun,
    JobRunFilters,
    UserExtensionSettings,  #
)

db = Database("ext_repay")


########################### Job Config ############################
async def create_job_config(user_id: str, data: CreateJobConfig) -> JobConfig:
    job_config = JobConfig(**data.dict(), id=urlsafe_short_hash(), user_id=user_id)
    await db.insert("repay.job_config", job_config)
    return job_config


async def get_job_config(
    user_id: str,
    job_config_id: str,
) -> JobConfig | None:
    return await db.fetchone(
        """
            SELECT * FROM repay.job_config
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": job_config_id, "user_id": user_id},
        JobConfig,
    )


async def get_job_config_by_id(
    job_config_id: str,
) -> JobConfig | None:
    return await db.fetchone(
        """
            SELECT * FROM repay.job_config
            WHERE id = :id
        """,
        {"id": job_config_id},
        JobConfig,
    )


async def get_job_config_ids_by_user(
    user_id: str,
) -> list[str]:
    rows: list[dict] = await db.fetchall(
        """
            SELECT DISTINCT id FROM repay.job_config
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
    )

    return [row["id"] for row in rows]


async def get_job_config_paginated(
    user_id: str | None = None,
    filters: Filters[JobConfigFilters] | None = None,
) -> Page[JobConfig]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM repay.job_config",
        where=where,
        values=values,
        filters=filters,
        model=JobConfig,
    )


async def get_all_enabled_job_configs() -> list[JobConfig]:
    # todo: cache
    return await db.fetchall(
        "SELECT * FROM repay.job_config WHERE enabled = true",
        model=JobConfig,
    )


async def update_job_config(data: JobConfig) -> JobConfig:
    await db.update("repay.job_config", data)
    return data


async def delete_job_config(user_id: str, job_config_id: str) -> None:
    await db.execute(
        """
            DELETE FROM repay.job_config
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": job_config_id, "user_id": user_id},
    )


################################# Job Run ###########################


async def create_job_run(job_config_id: str, data: CreateJobRun) -> JobRun:
    job_run = JobRun(**data.dict(), id=urlsafe_short_hash(), job_config_id=job_config_id)
    await db.insert("repay.job_run", job_run)
    return job_run


async def get_job_run(
    job_config_id: str,
    job_run_id: str,
) -> JobRun | None:
    return await db.fetchone(
        """
            SELECT * FROM repay.job_run
            WHERE id = :id AND job_config_id = :job_config_id
        """,
        {"id": job_run_id, "job_config_id": job_config_id},
        JobRun,
    )


async def get_job_run_by_id(
    job_run_id: str,
) -> JobRun | None:
    return await db.fetchone(
        """
            SELECT * FROM repay.job_run
            WHERE id = :id
        """,
        {"id": job_run_id},
        JobRun,
    )


async def get_job_run_paginated(
    job_config_ids: list[str] | None = None,
    filters: Filters[JobRunFilters] | None = None,
) -> Page[JobRun]:

    if not job_config_ids:
        return Page(data=[], total=0)

    where = []
    values = {}
    id_clause = []
    for i, item_id in enumerate(job_config_ids):
        # job_config_ids are not user input, but DB entries, so this is safe
        job_config_id = f"job_config_id__{i}"
        id_clause.append(f"job_config_id = :{job_config_id}")
        values[job_config_id] = item_id
    or_clause = " OR ".join(id_clause)
    where.append(f"({or_clause})")

    return await db.fetch_page(
        "SELECT * FROM repay.job_run",
        where=where,
        values=values,
        filters=filters,
        model=JobRun,
    )


async def update_job_run(data: JobRun) -> JobRun:
    await db.update("repay.job_run", data)
    return data


async def delete_job_run(job_config_id: str, job_run_id: str) -> None:
    await db.execute(
        """
            DELETE FROM repay.job_run
            WHERE id = :id AND job_config_id = :job_config_id
        """,
        {"id": job_run_id, "job_config_id": job_config_id},
    )


############################ Settings #############################
async def create_extension_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = UserExtensionSettings(**data.dict(), id=user_id)
    await db.insert("repay.extension_settings", settings)
    return settings


async def get_extension_settings(
    user_id: str,
) -> ExtensionSettings | None:
    return await db.fetchone(
        """
            SELECT * FROM repay.extension_settings
            WHERE id = :user_id
        """,
        {"user_id": user_id},
        ExtensionSettings,
    )


async def update_extension_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = UserExtensionSettings(**data.dict(), id=user_id)
    await db.update("repay.extension_settings", settings)
    return settings
