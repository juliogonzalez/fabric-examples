from boto import ec2
from fabric.api import run, sudo, task
from fabric.operations import local, prompt


@task
def uname():
    """ Prints the output of uname -a """
    run('uname -a')


@task
def cat_file(file_path=None, use_sudo=False):
    """ Prints the output of a file, optionally using sudo """
    if not file_path:
        file_path = prompt('Path to the file: ')
    command = 'cat %s' % file_path
    if sudo:
        sudo(command)
    else:
        run(command)


@task
def local_user():
    """ Prints the local user """
    local('whoami')


@task
def get_account_id(region='eu-west-1'):
    conn = ec2.connect_to_region(region)
    print(conn.get_all_security_groups()[0].owner_id)
