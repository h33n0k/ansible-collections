import os
import pytest


@pytest.fixture(scope='module')
def AnsibleVars(host):
    return host.ansible(
        'include_vars',
        '../../molecule/volume/defaults/main.yml'
    )['ansible_facts']


def test_mounted_volumes(host, AnsibleVars):
    volumes = AnsibleVars.get('docker_volumes')

    for volume in volumes:

        vol = host.file(volume['host'])
        group = volume.get('group', 'docker')
        parent_path = os.path.dirname(volume['host'])
        parent = host.file(parent_path)

        assert parent.is_directory
        assert parent.user == 'root'
        assert parent.group == 'docker'
        assert oct(parent.mode) == '0o2770'

        assert vol.exists
        assert vol.user == 'root'
        assert vol.group == group

        if volume['type'] == 'directory':
            assert vol.is_directory
            assert oct(vol.mode) == '0o2770'
            expected_acls = [
                'user::rwx',
                'user:root:rwx',
                'group::rwx',
                f'group:{group}:rwx',
                'other::---'
            ]
        else:
            assert oct(vol.mode) == '0o660'
            expected_acls = [
                'user::rw',
                'user:root:rw',
                'group::rw',
                f'group:{group}:rw',
                'other::---'
            ]

        getfacl = host.run(f"getfacl -p {volume['host']}")
        assert getfacl.rc == 0

        default_prefix = 'default:'
        for acl in expected_acls:
            assert acl in getfacl.stdout
            if volume['type'] == 'directory':
                assert f'{default_prefix}{acl}' in getfacl.stdout


def test_actl_mask(host, AnsibleVars):
    volumes = AnsibleVars.get('docker_volumes')
    directories = list(filter(lambda x: x.get('type') == 'directory', volumes))
    for volume in directories:
        f = f'{volume.get("host")}/testfile.txt'
        f_command = host.run(f'touch {f}')
        assert f_command.rc == 0
        file = host.file(f)
        assert file.exists
        assert file.user == 'root'
        assert file.group == volume.get('group', 'docker')
        assert oct(file.mode) == '0o660'

        d = f'{volume.get("host")}/testDir'
        d_command = host.run(f'mkdir {d}')
        assert d_command.rc == 0
        dir = host.file(d)
        assert dir.exists
        assert dir.user == 'root'
        assert dir.group == volume.get('group', 'docker')
        assert oct(dir.mode) == '0o2770'
