import pytest
import json


@pytest.fixture(scope='module')
def AnsibleVars(host):
    return host.ansible(
        'include_vars',
        '../../molecule/run/defaults/main.yml'
    )['ansible_facts']


def find_container_by_name(containers, name):
    for container_id, container_data in containers.items():
        if container_data.get('Name') == name:
            return container_data
    return None


# Check network creation and assignation
def test_docker_networks(host, AnsibleVars):
    container_config = AnsibleVars.get('docker_container')

    container_name = container_config.get('name')
    network_name = container_config.get('networks')[0].get('name')
    network_driver = container_config.get(
        'networks')[0].get('driver', 'default')

    networks = host.run("docker network ls | awk '{print $2}' | tail -n +2")
    assert networks.rc == 0
    assert network_name in networks.stdout

    inspect = host.run(f'docker network inspect {network_name}')
    assert inspect.rc == 0
    try:
        network = json.loads(inspect.stdout)
        container = find_container_by_name(
            network[0].get('Containers'),
            container_name
        )
        assert container is not None
        assert network[0].get('Driver', 'default') == network_driver

    except json.JSONDecodeError as e:
        pytest.fail(f'Invalid JSON in network inspect {network_name}: {e}')


def test_docker_container(host, AnsibleVars):
    container_config = AnsibleVars.get('docker_container')
    container_name = container_config.get('name')
    inspect = host.run(f"docker container inspect {container_name}")
    try:
        container = json.loads(inspect.stdout)[0]
        assert container is not None
        config = container.get('Config')
        state = container.get('State')
        hostConfig = container.get('HostConfig')

        assert state.get('Running')
        assert not state.get('Dead')
        assert container.get('Name') == f"/{container_config.get('name')}"
        assert config.get('Image') == container_config.get('image')

        assert hostConfig.get(
            'RestartPolicy').get('Name') == container_config.get('restart')

        containerBinds = hostConfig.get('Binds')
        assert not len(containerBinds) == 0
        for volume in container_config.get('volumes'):
            bind = ':'.join([
                volume.get('host'),
                volume.get('container'),
                volume.get('access'),
            ])
            assert bind in containerBinds

        containerPorts = [f"{int(binding['HostPort'])}:{int(container_port.split('/')[0])}"
                          for container_port, bindings in hostConfig.get('PortBindings').items()
                          for binding in bindings]

        assert not len(containerPorts) == 0
        for bind in container_config.get('ports'):
            assert bind in containerPorts

    except json.JSONDecodeError as e:
        pytest.fail(f'Invalid JSON in container inspect {container_name}: {e}')


def test_container_server(host):
    response = host.run('curl http://localhost')
    assert response.rc == 0
    assert response.stdout == '<p>Hello World</p>'


def test_volumes_permissions(host, AnsibleVars):
    container_config = AnsibleVars.get('docker_container')
    container_name = container_config.get('name')
    container_volume = container_config.get('volumes')[0]

    def checkFilesPermissions():
        files = host.run(f"find {container_volume.get('host')} -type f")
        assert files.rc == 0
        for path in files.stdout.strip().split('\n'):
            file = host.file(path)
            assert file.exists
            assert file.user == 'root'
            assert file.group == container_volume.get('group', 'docker')
            assert oct(file.mode) == '0o660'

    checkFilesPermissions()

    command = f"touch {container_volume.get('container')}/test.txt"
    sideCommand = host.run(f"docker exec {container_name} sh -c '{command}'")
    assert sideCommand.rc == 0

    checkFilesPermissions()
