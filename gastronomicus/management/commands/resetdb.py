from os.path import dirname, basename
from subprocess import check_output
from django.core.management.base import AppCommand
from south.models import MigrationHistory
 
class Command(AppCommand):
    help = "Clear app (with manage.py sqlclear) and south migrations for app"
    def handle_app(self, app, verbosity = 1, **options):
        printer = Printer(verbosity = verbosity)
        app_dir = dirname(app.__file__)
        app_name = basename(app_dir)

        printer('Clearing SQL for ' + app_name)
        cmd = 'python manage.py sqlclear %s | python manage.py dbshell' % app_name
        printer(check_output(cmd, shell=True), verbosity = 2)

        printer('Clearing south history (in south app SQL) for ' + app_name)
        MigrationHistory.objects.filter(app_name__exact=app_name).delete()

        printer('Clearing migration files')
        cmd = 'rm -f %s/migrations/*' % app_dir
        printer(check_output(cmd, shell=True), verbosity = 2)
 
class Printer(object):
    def __init__(self, verbosity = 1):
        self.verbosity = int(verbosity)

    def __call__(self, s, verbosity = 1, prefix = '***'):
        if verbosity <= self.verbosity:
            print prefix, s
