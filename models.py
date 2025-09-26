from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, Field


########################### Job Config ############################
class CreateJobConfig(BaseModel):
    name: str
    description: str | None = None
    minutes: int | None = None
    hours: int | None = None
    day_of_month: int | None = None
    month: int | None = None
    day_of_week: int | None = None
    pay_from_wallet_id: str
    pay_to: str
    currency: str = "sat"
    amount: float
    enabled: bool | None = None


class JobConfig(BaseModel):
    id: str
    user_id: str
    name: str
    description: str | None = None
    minutes: int | None = None
    hours: int | None = None
    day_of_month: int | None = None
    month: int | None = None
    day_of_week: int | None = None
    pay_from_wallet_id: str
    pay_to: str
    currency: str = "sat"
    amount: float
    enabled: bool | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def match_cron(self, dt: datetime) -> bool:
        print("### self", [self.minutes, self.hours, self.day_of_month, self.month, self.day_of_week])
        print("### cron", [dt.minute, dt.hour, dt.day, dt.month, dt.weekday()])
        if not self.enabled:
            return False
        if self.minutes is not None and self.minutes != dt.minute:
            return False
        if self.hours is not None and self.hours != dt.hour:
            return False
        if self.day_of_month is not None and self.day_of_month != dt.day:
            return False
        if self.month is not None and self.month != dt.month:
            return False
        if self.day_of_week is not None and self.day_of_week != dt.weekday():
            return False
        return True


class JobConfigFilters(FilterModel):
    __search_fields__ = [
        "name",
        "description",
        "minutes",
        "hours",
        "day_of_month",
        "month",
        "day_of_week",
        "pay_from_wallet_id",
        "pay_to",
        "currency",
        "amount",
        "enabled",
    ]

    __sort_fields__ = [
        "name",
        "description",
        "minutes",
        "hours",
        "day_of_month",
        "month",
        "day_of_week",
        "pay_from_wallet_id",
        "pay_to",
        "currency",
        "amount",
        "enabled",
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


################################# Job Run ###########################


class CreateJobRun(BaseModel):
    name: str | None
    success: bool
    status_text: str | None
    duration_seconds: int
    payment_hash: str


class JobRun(BaseModel):
    id: str
    job_config_id: str
    name: str | None
    success: bool
    status_text: str | None
    duration_seconds: int
    payment_hash: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobRunFilters(FilterModel):
    __search_fields__ = [
        "name",
        "success",
        "status_text",
        "duration_seconds",
        "payment_hash",
    ]

    __sort_fields__ = [
        "name",
        "success",
        "status_text",
        "duration_seconds",
        "payment_hash",
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


############################ Settings #############################
class ExtensionSettings(BaseModel):
    name: str | None = None

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def is_admin_only(cls) -> bool:
        return bool("False" == "True")


class UserExtensionSettings(ExtensionSettings):
    id: str
