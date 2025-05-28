import pytest


@pytest.fixture(scope='module')
def AnsibleVars(host):
    return host.ansible(
        'include_vars',
        '../../defaults/main.yml'
    )['ansible_facts']


def test_installed_packages(host):
    packages = ['ufw']
    for p in packages:
        package = host.package(p)
        assert package.is_installed, \
            f'package {p} should have been installed'


def test_enabled_services(host):
    services = ['ufw']
    for s in services:
        service = host.service(s)
        assert service.is_running, \
            f'service {s} should be running'
        assert service.is_enabled, \
            f'service {s} should be enabled'


def test_ufw_status(host):
    cmd = host.run('ufw status')
    assert cmd.rc == 0
    assert 'Status: active' in cmd.stdout


def test_ufw_policies(host, AnsibleVars):
    incoming = AnsibleVars.get('firewall_incoming_policy')
    outgoing = AnsibleVars.get('firewall_outgoing_policy')
    cmd = host.run('ufw status verbose')
    assert f'{incoming} (incoming)' in cmd.stdout
    assert f'{outgoing} (outgoing)' in cmd.stdout


def test_ufw_ipv6_status(host, AnsibleVars):
    enabled = AnsibleVars.get('firewall_disable_ipv6')
    config = host.file('/etc/default/ufw')
    assert config.exists
    assert config.contains(f"IPV6={'no' if enabled else 'yes'}")


def test_ufw_allowed_ports(host, AnsibleVars):
    ports = AnsibleVars.get('firewall_allow_ports')
    status = host.run('ufw status numbered')
    for port in ports:
        assert port in status.stdout
