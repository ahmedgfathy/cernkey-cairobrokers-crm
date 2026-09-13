from django.apps import AppConfig
from django.db.backends.signals import connection_created


def configure_sqlite_connection(sender, connection, **kwargs):
    """Allow concurrent reads while imports are writing to SQLite."""
    if connection.vendor != 'sqlite':
        return
    with connection.cursor() as cursor:
        cursor.execute('PRAGMA busy_timeout = 30000')
        cursor.execute('PRAGMA journal_mode = WAL')


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        connection_created.connect(
            configure_sqlite_connection,
            dispatch_uid='core.configure_sqlite_connection',
        )
