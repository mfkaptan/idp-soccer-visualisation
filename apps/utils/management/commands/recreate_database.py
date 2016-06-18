import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.utils import ConnectionDoesNotExist


class Command(BaseCommand):
    help = 'Recreates the database'

    def add_arguments(self, parser):
        parser.add_argument('--database',
                            action='store',
                            dest='database',
                            default='default',
                            help='Database connection name')

    def handle(self, *args, **options):
        try:
            connection = connections[options['database']]
            cursor = connection.cursor()
            database_settings = settings.DATABASES[options['database']]
        except ConnectionDoesNotExist:
            raise CommandError('Database "%s" does not exist in settings' % options['database'])


        print("Dropping and recreating schema public")
        cursor.execute("DROP schema public CASCADE; CREATE schema public")

