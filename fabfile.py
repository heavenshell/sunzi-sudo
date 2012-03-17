# -*- coding: utf-8 -*-
"""
    Sunzi-sudo
    ~~~~~~~~~~

    Wrapper Fabric script for Sunzi.

    `Sunzi <https://github.com/kenn/sunzi>`_ is the easiest server
    provisioning tool written in Ruby.

    Sunzi-sudo is simple wrapper to enable use sudo.

    Sunzi always use the root user, but if you want to use sudo,
    use Sunzi-sudo.


    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import re
import yaml
from fabric.api import local, sudo, task, hide, env, put, run
from fabric.colors import red


@task
def sunzi(bundle=None, host=None, user=None):
    if env.host_string != '':
        host = env.host_string

    if env.user != '':
        user = env.user

    if host is None and user is None:
        msg = '"deploy" was called incorrectly. '
        msg += 'Call as "sunzi deploy [user@host:port] [role]".'
        print(red(msg))
        return

    if bundle is None:
        local('sunzi compile')
    else:
        local('bundle exec sunzi compile')

    with hide('running'):
        local('rm -f sunzi.tar.gz')
        local('tar cfz sunzi.tar.gz compiled')

        user, host, port = _parse_target(host)

        local('ssh-keygen -R %s 2> /dev/null' % host)

        if env.host_string == '':
            env.host_string = host
        env.port = port

        path = os.path.dirname(os.path.abspath(__file__))
        put(os.path.join(path, 'sunzi.tar.gz'), '~/sunzi.tar.gz')
        run('rm -rf sunzi')
        run('tar xzf sunzi.tar.gz')
        run('mv compiled sunzi')
        run('rm sunzi.tar.gz')
        sudo('cd sunzi && bash install.sh', pty=True)

    preference = _parse_config()
    if preference is not None and preference['erase_remote_folder']:
        with hide('running'):
            run('rm -rf ~/sunzi')


def _parse_target(target):
    r = re.compile('(.*@)?(.*?)(:.*)?$')
    result = r.match(target)
    user = 'root' if result.group(1) is None else result.group(1).rstrip('@')
    host = result.group(2)
    port = '22' if result.group(3) is None else result.group(3).lstrip(':')

    return user, host, port


def _parse_config():
    with open('sunzi.yml') as f:
        data = yaml.load(f)
        if 'preferences' in data:
            return data['preferences']

    return None
