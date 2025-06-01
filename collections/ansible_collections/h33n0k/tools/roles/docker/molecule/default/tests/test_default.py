import pytest
import json


@pytest.fixture(scope='module')
def AnsibleVars(host):
    return host.ansible(
        'include_vars',
        '../../defaults/main.yml'
    )['ansible_facts']


def test_packages_installation(host):
    packages = [
        'ca-certificates',
        'gnupg',
        'lsb-release',
        'docker-ce',
        'docker-ce-cli',
        'containerd.io',
        'docker-buildx-plugin',
        'docker-compose-plugin'
    ]

    for p in packages:
        package = host.package(p)
        assert package.is_installed


def test_docker_key(host):
    directory = host.file('/etc/apt/keyrings')
    key = host.file('/etc/apt/keyrings/docker.asc')
    for file in [directory, key]:
        assert file.exists
        assert file.user == 'root'
        assert file.group == 'adm'
    source = host.file('/etc/apt/sources.list.d/docker.list')
    assert source.exists
    assert directory.mode == 0o655
    assert key.mode == 0o644


def test_enabled_services(host):
    service = host.service('docker')
    assert service.is_running
    assert service.is_enabled


def test_daemon_template(host, AnsibleVars):
    file = host.file('/etc/docker/daemon.json')
    assert file.exists, \
        f'{file.path} should have been deployed'
    assert file.mode == 0o660
    assert file.user == 'root'
    assert file.group == 'adm'

    try:
        content = json.loads(file.content_string)
    except json.JSONDecodeError as e:
        pytest.fail(f'Invalid JSON in {file.path}: {e}')

    options = {
        'iptables': AnsibleVars.get('docker_iptables')
    }

    for key in options.keys():
        assert key in content
        assert content[key] == options[key]
