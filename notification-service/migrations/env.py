import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Load Alembic Config
config = context.config

# Logging
fileConfig(config.config_file_name)

# Use env var or default DB URL
db_url = os.getenv("DATABASE_URL", "postgresql://group3:group3pass@postgres/notification_db")
config.set_main_option("sqlalchemy.url", db_url)

# Import your models
from app.models import db  # Adjust if your db is elsewhere

target_metadata = db.metadata  # Needed for autogenerate support


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

