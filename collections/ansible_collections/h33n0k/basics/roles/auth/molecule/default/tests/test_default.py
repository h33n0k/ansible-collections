import pytest


@pytest.fixture(scope='module')
def AnsibleVars(host):
    return host.ansible(
        'include_vars',
        '../../defaults/main.yml'
    )['ansible_facts']


def test_ssh_group(host, AnsibleVars):
    group = host.group('ssh')
    gid = AnsibleVars.get('auth_ssh_group_gid')
    assert group.exists, \
        f'group {group.name} should have been added.'
    assert group.gid == gid, \
        f'{group.name} gid should be {gid}'


def test_users_creation(host, AnsibleVars):
    users = AnsibleVars.get('auth_users')
    for user in users:
        u = host.user(user['username'])
        assert u.exists, \
            f"user {user['username']} should have been added."
        home = host.file(f"/home/{user['username']}")
        assert home.exists == user['home']
        if user['home']:
            assert home.user == user['username']
            assert home.group == user['username']

        for group in user['groups']:
            assert group in u.groups, \
                f"user {user['username']} should be in group {group}"


def test_ssh_server_package(host):
    package = host.package('openssh-server')
    assert package.is_installed, \
        'openssh-server should have been installed.'


def test_ssh_rsyslog(host):
    file = host.file('/etc/rsyslog.d/sshd.conf')
    assert file.exists, \
        'rsyslog configuration should have been deployed.'
    assert file.user == 'root'
    assert file.group == 'adm'
    assert file.mode == 0o644


def test_sshd_config(host):
    file = host.file('/etc/ssh/sshd_config')
    assert file.exists, \
        'sshd configuration should have been deployed.'
    assert file.user == 'root'
    assert file.group == 'adm'
    assert file.mode == 0o644


def test_ssh_permissions(host, AnsibleVars):
    users = AnsibleVars.get('auth_users')
    for user in users:
        if 'ssh' in user['groups']:
            directory = host.file(f"/home/{user['username']}/.ssh")
            assert directory.exists
            assert directory.user == user['username']
            assert directory.group == user['username']
            assert directory.mode == 0o700


def test_sshd_service(host):
    service = host.service('sshd')
    assert service.is_running
    assert service.is_enabled


def test_fail2ban_jail(host):
    files = [
        '/etc/fail2ban/jail.d/sshd.local',
        '/etc/fail2ban/filter.d/sshd.local'
    ]

    for f in files:
        file = host.file(f)
        assert file.exists
        assert file.mode == 0o644
        assert file.user == 'root'
        assert file.group == 'adm'

    status = host.run('fail2ban-client status')
    assert 'sshd' in status.stdout


def test_fail2ban_service(host):
    service = host.service('fail2ban')
    assert service.is_running
    assert service.is_enabled
