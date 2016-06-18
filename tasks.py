import os

from invoke import run, task

DEFAULT_PYTHON = '3.4'  # Used in virtualenv

DIR = os.path.dirname(os.path.realpath(__file__))
VENV = os.path.join(DIR, 'env')
PIP = os.path.join(VENV, 'bin/pip')
MANAGE = os.path.join(VENV, 'bin/python') + ' ' + os.path.join(DIR, 'manage.py')
NODE = os.path.join(DIR, 'node_modules')


@task
def clean():
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
def prepare():
    """
    Creates empty directories for logs, etc
    """
    dirs = [
        '../log',
        'static',
    ]
    run('mkdir -p %s' % ' '.join([os.path.join(DIR, d) for d in dirs]))


@task
def gitmodules():
    """
    Initializes and updates gitmodules
    """
    run('git submodule init')
    run('git submodule sync')
    run('git submodule update')


@task
def virtualenv(pyversion=DEFAULT_PYTHON):
    """
    Creates a virtualenv with the provided Python version
    :param pyversion:
    """
    run('virtualenv -p /usr/bin/python' + pyversion + ' env')


@task
def requirements():
    """
    Installs requirements, optionally for the development environment
    :param env:
    """
    run(PIP + ' install -r requirements.txt')


@task
def setup(pyversion=DEFAULT_PYTHON):
    """
    Runs all setup tasks (no management commands)
    :param pyversion:
    :param env:
    """
    if not os.path.isdir(VENV):
        virtualenv(pyversion=pyversion)
    requirements()


@task
def db_recreate():
    """
    Drops and recreates the database
    """
    run(MANAGE + ' recreate_database')


@task
def db_migrate():
    """
    Runs database migrations
    """
    run(MANAGE + ' migrate --noinput')


@task
def db():
    """
    Runs all database tasks
    :param recreate:
    """
    db_recreate()

    db_migrate()


@task
def migrations():
    run(MANAGE + ' makemigrations')

    run(MANAGE + ' migrate')


@task
def import_match():
    print("Importing matches")
    run(MANAGE + ' import_matchinformation /home/kaptan/workspace/idp/TRACAB/MatchInformation__DFL-MAT-0025I9.xml')


@task
def import_events():
    print("Importing events")
    run(MANAGE + ' import_events /home/kaptan/workspace/idp/TRACAB/Events_DFL-MAT-0025I9.xml')


@task(default=True)
def main(pyversion=DEFAULT_PYTHON, all=False, migrate=False, xml=False):
    """
    Does a full build for a python version and environment
    :param pyversion:
    :param env:
    """
    setup(pyversion=pyversion)
    db()

    if all or migrate:
        migrations()

    if all or xml:
        import_match()
        import_events()
