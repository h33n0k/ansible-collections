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
