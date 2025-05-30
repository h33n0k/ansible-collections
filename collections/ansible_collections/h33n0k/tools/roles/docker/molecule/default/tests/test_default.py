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
