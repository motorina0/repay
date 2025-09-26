# Description: This file contains the extensions API endpoints.
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.core.models import SimpleStatus, User
from lnbits.db import Filters, Page
from lnbits.decorators import (
    check_user_exists,
    parse_filters,
)
from lnbits.helpers import generate_filter_params_openapi

from .crud import (
    create_job_config,
    create_job_run,
    delete_job_config,
    delete_job_run,
    get_job_config,
    get_job_config_ids_by_user,
    get_job_config_paginated,
    get_job_run_by_id,
    get_job_run_paginated,
    update_job_config,
    update_job_run,
)
from .models import (
    CreateJobConfig,
    CreateJobRun,
    ExtensionSettings,  #
    JobConfig,
    JobConfigFilters,
    JobRun,
    JobRunFilters,
)
from .services import (
    get_settings,  #
    update_settings,  #
)

job_config_filters = parse_filters(JobConfigFilters)
job_run_filters = parse_filters(JobRunFilters)

repay_api_router = APIRouter()


############################# Job Config #############################
@repay_api_router.post("/api/v1/job_config", status_code=HTTPStatus.CREATED)
async def api_create_job_config(
    data: CreateJobConfig,
    user: User = Depends(check_user_exists),
) -> JobConfig:
    job_config = await create_job_config(user.id, data)
    return job_config


@repay_api_router.put("/api/v1/job_config/{job_config_id}", status_code=HTTPStatus.CREATED)
async def api_update_job_config(
    job_config_id: str,
    data: CreateJobConfig,
    user: User = Depends(check_user_exists),
) -> JobConfig:
    job_config = await get_job_config(user.id, job_config_id)
    if not job_config:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Job Config not found.")
    if job_config.user_id != user.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this job config.")
    job_config = await update_job_config(JobConfig(**{**job_config.dict(), **data.dict()}))
    return job_config


@repay_api_router.get(
    "/api/v1/job_config/paginated",
    name="Job Config List",
    summary="get paginated list of job_config",
    response_description="list of job_config",
    openapi_extra=generate_filter_params_openapi(JobConfigFilters),
    response_model=Page[JobConfig],
)
async def api_get_job_config_paginated(
    user: User = Depends(check_user_exists),
    filters: Filters = Depends(job_config_filters),
) -> Page[JobConfig]:

    return await get_job_config_paginated(
        user_id=user.id,
        filters=filters,
    )


@repay_api_router.get(
    "/api/v1/job_config/{job_config_id}",
    name="Get JobConfig",
    summary="Get the job_config with this id.",
    response_description="An job_config or 404 if not found",
    response_model=JobConfig,
)
async def api_get_job_config(
    job_config_id: str,
    user: User = Depends(check_user_exists),
) -> JobConfig:

    job_config = await get_job_config(user.id, job_config_id)
    if not job_config:
        raise HTTPException(HTTPStatus.NOT_FOUND, "JobConfig not found.")

    return job_config


@repay_api_router.delete(
    "/api/v1/job_config/{job_config_id}",
    name="Delete Job Config",
    summary="Delete the job_config " "and optionally all its associated job_run.",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_job_config(
    job_config_id: str,
    clear_job_run: bool | None = False,
    user: User = Depends(check_user_exists),
) -> SimpleStatus:

    await delete_job_config(user.id, job_config_id)
    if clear_job_run is True:
        # await delete all job run associated with this job config
        pass
    return SimpleStatus(success=True, message="Job Config Deleted")


############################# Job Run #############################
@repay_api_router.post(
    "/api/v1/job_run/{job_config_id}",
    name="Create Job Run",
    summary="Create new job run for the specified job config.",
    response_description="The created job run.",
    response_model=JobRun,
    status_code=HTTPStatus.CREATED,
)
async def api_create_job_run(
    job_config_id: str,
    data: CreateJobRun,
    user: User = Depends(check_user_exists),
) -> JobRun:
    job_config = await get_job_config(user.id, job_config_id)
    if not job_config:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Job Config not found.")

    job_run = await create_job_run(job_config_id, data)
    return job_run


@repay_api_router.put(
    "/api/v1/job_run/{job_run_id}",
    name="Update Job Run",
    summary="Update the job_run with this id.",
    response_description="The updated job run.",
    response_model=JobRun,
)
async def api_update_job_run(
    job_run_id: str,
    data: CreateJobRun,
    user: User = Depends(check_user_exists),
) -> JobRun:
    job_run = await get_job_run_by_id(job_run_id)
    if not job_run:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Job Run not found.")

    job_config = await get_job_config(user.id, job_run.job_config_id)
    if not job_config:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Job Config not found.")

    job_run = await update_job_run(JobRun(**{**job_run.dict(), **data.dict()}))
    return job_run


@repay_api_router.get(
    "/api/v1/job_run/paginated",
    name="Job Run List",
    summary="get paginated list of job_run",
    response_description="list of job_run",
    openapi_extra=generate_filter_params_openapi(JobRunFilters),
    response_model=Page[JobRun],
)
async def api_get_job_run_paginated(
    user: User = Depends(check_user_exists),
    job_config_id: str | None = None,
    filters: Filters = Depends(job_run_filters),
) -> Page[JobRun]:

    job_config_ids = await get_job_config_ids_by_user(user.id)

    if job_config_id:
        if job_config_id not in job_config_ids:
            raise HTTPException(HTTPStatus.FORBIDDEN, "Not your job config.")
        job_config_ids = [job_config_id]

    return await get_job_run_paginated(
        job_config_ids=job_config_ids,
        filters=filters,
    )


@repay_api_router.get(
    "/api/v1/job_run/{job_run_id}",
    name="Get Job Run",
    summary="Get the job run with this id.",
    response_description="An job run or 404 if not found",
    response_model=JobRun,
)
async def api_get_job_run(
    job_run_id: str,
    user: User = Depends(check_user_exists),
) -> JobRun:

    job_run = await get_job_run_by_id(job_run_id)
    if not job_run:
        raise HTTPException(HTTPStatus.NOT_FOUND, "JobRun not found.")
    job_config = await get_job_config(user.id, job_run.job_config_id)
    if not job_config:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Job Config deleted for this Job Run.")

    return job_run


@repay_api_router.delete(
    "/api/v1/job_run/{job_run_id}",
    name="Delete Job Run",
    summary="Delete the job_run",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_job_run(
    job_run_id: str,
    user: User = Depends(check_user_exists),
) -> SimpleStatus:

    job_run = await get_job_run_by_id(job_run_id)
    if not job_run:
        raise HTTPException(HTTPStatus.NOT_FOUND, "JobRun not found.")
    job_config = await get_job_config(user.id, job_run.job_config_id)
    if not job_config:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Job Config deleted for this Job Run.")

    await delete_job_run(job_config.id, job_run_id)
    return SimpleStatus(success=True, message="Job Run Deleted")


############################ Settings #############################
@repay_api_router.get(
    "/api/v1/settings",
    name="Get Settings",
    summary="Get the settings for the current user.",
    response_description="The settings or 404 if not found",
    response_model=ExtensionSettings,
)
async def api_get_settings(
    user: User = Depends(check_user_exists),
) -> ExtensionSettings:
    user_id = "admin" if ExtensionSettings.is_admin_only() else user.id
    return await get_settings(user_id)


@repay_api_router.put(
    "/api/v1/settings",
    name="Update Settings",
    summary="Update the settings for the current user.",
    response_description="The updated settings.",
    response_model=ExtensionSettings,
)
async def api_update_extension_settings(
    data: ExtensionSettings,
    user: User = Depends(check_user_exists),
) -> ExtensionSettings:
    if ExtensionSettings.is_admin_only() and not user.admin:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            "Only admins can update settings.",
        )
    user_id = "admin" if ExtensionSettings.is_admin_only() else user.id
    return await update_settings(user_id, data)
