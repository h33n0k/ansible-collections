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
        assert oct(vol.mode) == '0o2770'

        if volume['type'] == 'directory':
            assert vol.is_directory

        expected_acls = [
            'user::rwx',
            'user:root:rwx',
            'group::rwx',
            f'group:{group}:rwx',
            'other::---'
        ]

        getfacl = host.run(f"getfacl -p {volume['host']}")
        assert getfacl.rc == 0

        default_prefix = 'default:'
        for acl in expected_acls:
            assert acl in getfacl.stdout
            if volume['type'] == 'directory':
                assert f'{default_prefix}{acl}' in getfacl.stdout
