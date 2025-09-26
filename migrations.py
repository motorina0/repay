# the migration file is where you build your database tables
# If you create a new release for your extension ,
# remember the migration file is like a blockchain, never edit only add!

empty_dict: dict[str, str] = {}


async def m001_extension_settings(db):
    """
    Initial settings table.
    """

    await db.execute(
        f"""
        CREATE TABLE repay.extension_settings (
            id TEXT NOT NULL,
            name TEXT,
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


async def m002_job_config(db):
    """
    Initial job config table.
    """

    await db.execute(
        f"""
        CREATE TABLE repay.job_config (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            minutes INT,
            hours INT,
            day_of_month INT,
            month INT,
            day_of_week INT,
            pay_from_wallet_id TEXT NOT NULL,
            pay_to TEXT NOT NULL,
            currency TEXT NOT NULL,
            amount REAL NOT NULL,
            enabled BOOLEAN,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


async def m003_job_run(db):
    """
    Initial job run table.
    """

    await db.execute(
        f"""
        CREATE TABLE repay.job_run (
            id TEXT PRIMARY KEY,
            job_config_id TEXT NOT NULL,
            name TEXT,
            success BOOLEAN NOT NULL,
            status_text TEXT,
            duration_seconds INT NOT NULL,
            payment_hash TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )
