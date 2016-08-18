import os

from invoke import run, task

DEFAULT_PYTHON = '3.5'  # Used in virtualenv

DIR = os.path.dirname(os.path.realpath(__file__))
VENV = os.path.join(DIR, 'env')
PIP = os.path.join(VENV, 'bin/pip')
MANAGE = os.path.join(VENV, 'bin/python') + ' ' + os.path.join(DIR, 'manage.py')
NODE = os.path.join(DIR, 'node_modules')


@task
def clean(ctx):
    """
    Removes generate directories and compiled files
    """
    patterns = [
        'static',
        'env',
        '**/*.pyc',
    ]
    run('rm -rf %s' % ' '.join(patterns))


@task
def prepare(ctx):
    """
    Creates empty directories for logs, etc
    """
    dirs = [
        '../log',
        'static',
    ]
    run('mkdir -p %s' % ' '.join([os.path.join(DIR, d) for d in dirs]))


@task
def gitmodules(ctx):
    """
    Initializes and updates gitmodules
    """
    run('git submodule init')
    run('git submodule sync')
    run('git submodule update')


@task
def virtualenv(ctx, pyversion=DEFAULT_PYTHON):
    """
    Creates a virtualenv with the provided Python version
    :param pyversion:
    """
    run('virtualenv -p /usr/bin/python' + pyversion + ' env')


@task
def requirements(ctx):
    """
    Installs requirements, optionally for the development environment
    :param env:
    """
    run(PIP + ' install -r requirements.txt')


@task
def static(ctx, chmod=False):
    """
    Collects static files and optionally compresses them end sets permissive file permissions for webservers
    :param chmod:
    """
    run(MANAGE + ' collectstatic --noinput')
    if chmod:
        run('chmod -R 755 %s' % ' '.join([os.path.join(DIR, d) for d in ['media', 'static']]))


@task
def setup(ctx, pyversion=DEFAULT_PYTHON):
    """
    Runs all setup tasks (no management commands)
    :param pyversion:
    :param env:
    """
    if not os.path.isdir(VENV):
        virtualenv(ctx, pyversion=pyversion)
    requirements(ctx)


@task
def db_recreate(ctx):
    """
    Drops and recreates the database
    """
    run(MANAGE + ' recreate_database')


@task
def db_migrate(ctx):
    """
    Runs database migrations
    """
    run(MANAGE + ' migrate --noinput')


@task
def db(ctx, recreate=False):
    """
    Runs all database tasks
    :param recreate:
    """
    if recreate:
        db_recreate(ctx)

    db_migrate(ctx)


@task
def migrations(ctx):
    run(MANAGE + ' makemigrations')

    run(MANAGE + ' migrate')


@task
def import_match(ctx):
    print("Importing matches")
    run(MANAGE + ' import_matchinformation /home/kaptan/workspace/idp/TRACAB/MatchInformation__DFL-MAT-0025I9.xml')


@task
def import_events(ctx):
    print("Importing events")
    run(MANAGE + ' import_events /home/kaptan/workspace/idp/TRACAB/Events_DFL-MAT-0025I9.xml')


@task(default=True)
def main(ctx, pyversion=DEFAULT_PYTHON, reset=False, migrate=False, xml=False):
    """
    Does a full build for a python version and environment
    :param pyversion:
    :param env:
    """
    setup(ctx, pyversion=pyversion)
    db(ctx, recreate=reset)
    static(ctx, chmod=False)

    if reset or migrate:
        migrations(ctx)

    if reset or xml:
        import_match(ctx)
        import_events(ctx)
