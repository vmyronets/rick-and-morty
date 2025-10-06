import time
from psycopg import OperationalError as PsycopgError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for a database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        retry_count = 0
        max_retries = 30

        while db_up is False and retry_count < max_retries:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgError, OperationalError) as e:
                retry_count += 1
                self.stdout.write(
                    f'Database unavailable '
                    f'(attempt {retry_count}/{max_retries}), '
                    f'waiting 2 seconds... Error: {str(e)[:100]}'
                )
                time.sleep(2)

        if db_up:
            self.stdout.write(self.style.SUCCESS('Database available!'))
        else:
            self.stdout.write(
                self.style.ERROR(
                    f'Database failed to become available '
                    f'after {max_retries} attempts'
                )
            )
            raise OperationalError('Database connection failed')
