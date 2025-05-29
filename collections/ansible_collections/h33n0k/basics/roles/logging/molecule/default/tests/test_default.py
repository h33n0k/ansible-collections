# ---
# rsyslog assertions:

# Ensure that the rsyslog package is installed
def test_rsyslog_installation(host):
    package = host.package('rsyslog')
    assert package.is_installed, \
        'rsyslog package must be installed'


# Ensure the rsyslog configuration file exists
# and has the correct permissions and ownership
def test_rsyslog_conf_permissions(host):
    file = host.file('/etc/rsyslog.conf')
    assert file.exists, \
        'rsyslog configuration should exist'

    assert file.user == 'root'
    assert file.group == 'adm'
    assert file.mode == 0o640


# Ensure the rsyslog service is enabled and started
def test_rsyslog_service(host):
    service = host.service('rsyslog')
    assert service.is_enabled, \
        'rsyslog service should be enabled'
    assert service.is_running, \
        'rsyslog service should be started'


# ---
# auditd assertions:

# Ensure that the auditd packages are installed
def test_auditd_installation(host):
    packages = ['auditd', 'audispd-plugins']

    for package in packages:
        pkg = host.package(package)
        assert pkg.is_installed, \
            f'{package} package must be installed'


# Ensure the rsyslog configuration file exists
# and has the correct permissions and ownership
def test_auditd_conf_permissions(host):
    file = host.file('/etc/audit/auditd.conf')
    assert file.exists, \
        'auditd configuration should exist'

    assert file.user == 'root'
    assert file.group == 'adm'
    assert file.mode == 0o640


# ---
# logrotate assertions

# Ensure the logrotate configuration file exists
# and has the correct permissions and ownership
def test_logrotate_conf_permissions(host):
    file = host.file('/etc/logrotate.conf')
    assert file.exists, \
        'logrotate configuration should exist'
    assert file.user == 'root'
    assert file.group == 'adm'
    assert file.mode == 0o640


def test_logrotate_status(host):
    file = host.file('/var/lib/logrotate/status')
    assert file.exists, \
        'logrotate status file should exist'
