import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery(celery_type, celery_settings, extra_arguments, pids):
    starter_celery_cmd = 'celery {} -l info -A {} {}'.format(celery_type, celery_settings, extra_arguments)
    kill_worker_cmd = 'pkill -9 -f "{}"'.format(starter_celery_cmd)
    subprocess.call(shlex.split(kill_worker_cmd))
    subprocess.call(shlex.split(starter_celery_cmd))


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            'type', help='Celery type "beat" or "worker', choices={'beat', 'worker'}
        )
        parser.add_argument(
            '--celerysettings', dest='celery_settings', type=str,
            help='Tells Django to use celery settings', required=True
        )
        parser.add_argument(
            '--autoreload', action='store_true', dest='use_reloader',
            help='Tells Django to use the auto-reloader',
        )
        parser.add_argument(
            '--extra', dest='extra_args',
            help='Celery extra arguments"'
        )

    def handle(self, *args, **options):
        if options.get('use_reloader'):
            self.stdout.write('Starting celery with autoreload...')
            autoreload.main(restart_celery, args=(
                options.get('type'), options.get('celery_settings'), options.get('extra_args', ''), []
            ))
        else:
            self.stdout.write('Starting celery...')
            restart_celery(options.get('type'), options.get('celery_settings'), options.get('extra_args', ''), []),
