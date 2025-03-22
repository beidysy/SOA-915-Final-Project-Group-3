from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from flask import current_app
import os

# Alembic Config object
config = context.config

# Setup loggers
#fileConfig(config.config_file_name)
fileConfig(os.path.join(os.path.dirname(__file__), '../alembic.ini'))

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = current_app.extensions['migrate'].db.engine.url
    context.configure(
        url=url,
        target_metadata=current_app.extensions['migrate'].db.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    with current_app.app_context():
        connectable = current_app.extensions['migrate'].db.engine
        target_metadata = current_app.extensions['migrate'].db.metadata

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    with current_app.app_context():
        run_migrations_offline()
else:
    run_migrations_online()

