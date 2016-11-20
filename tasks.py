import os

from invoke import  task


DEFAULT_PYTHON = '3'  # Used in virtualenv

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
    ctx.run('rm -rf %s' % ' '.join(patterns))


@task
def prepare(ctx):
    """
    Creates empty directories for logs, etc
    """
    dirs = [
        '../log',
        'static',
    ]
    ctx.run('mkdir -p %s' % ' '.join([os.path.join(DIR, d) for d in dirs]))


@task
def virtualenv(ctx, pyversion=DEFAULT_PYTHON):
    """
    Creates a virtualenv with the provided Python version
    :param pyversion:
    """
    ctx.run('virtualenv -p /usr/bin/python' + pyversion + ' env')


@task
def requirements(ctx):
    """
    Installs requirements, optionally for the development environment
    :param env:
    """
    ctx.run(PIP + ' install -r requirements.txt')


@task
def static(ctx, chmod=False):
    """
    Collects static files and optionally compresses them and sets permissive file permissions for webservers
    :param chmod:
    """
    ctx.run(MANAGE + ' collectstatic --noinput')
    if chmod:
        ctx.run('chmod -R 755 %s' % ' '.join([os.path.join(DIR, d) for d in ['media', 'static']]))


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
def db(ctx):
    """
    Runs database migrations
    """
    ctx.run(MANAGE + ' migrate --noinput')


@task
def migrations(ctx):
    ctx.run(MANAGE + ' makemigrations')

    ctx.run(MANAGE + ' migrate')


@task
def import_match(ctx):
    print("Importing matches")
    ctx.run(MANAGE + ' import_matchinformation data/MatchInformation__DFL-MAT-0025I9.xml')


@task
def import_events(ctx):
    print("Importing events")
    ctx.run(MANAGE + ' import_events data/Events_DFL-MAT-0025I9.xml')


@task(default=True)
def main(ctx, pyversion=DEFAULT_PYTHON, migrate=False, xml=False):
    """
    Does a full build for a python version and environment
    :param pyversion:
    :param env:
    """
    setup(ctx, pyversion=pyversion)
    db(ctx)
    static(ctx, chmod=False)

    if migrate:
        migrations(ctx)

    if xml:
        import_match(ctx)
        import_events(ctx)
