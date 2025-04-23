import pytest


@pytest.fixture(scope='module')
def AnsibleDefaults(host):
    return host.ansible(
        'include_vars',
        '../../defaults/main.yml'
    )['ansible_facts']


# ---
# timesyncd assertions:

# Ensure that the systemd-timesyncd package is installed
def test_timesyncd_installation(host):
    package = host.package('systemd-timesyncd')
    assert package.is_installed, 'systemd-timesyncd package must be installed'


# Check that the systemd-timesyncd binary exists at the expected path
def test_timesyncd_binary(host):
    file = host.file('/lib/systemd/systemd-timesyncd')
    assert file.exists, 'systemd-timesyncd binary must be present'


# Validate that the timesyncd.conf configuration file exists
# and has the correct permissions and ownership
def test_timesyncd_conf_permissions(host):
    file = host.file('/etc/systemd/timesyncd.conf')
    assert file.exists, 'timesyncd.conf should exist'
    assert file.user == 'root'
    assert file.group == 'adm'
    assert file.mode == 0o644


# Ensure the systemd-timesyncd service is enabled and started
def test_timesyncd_service(host):
    service = host.service('systemd-timesyncd')
    assert service.is_enabled, 'systemd-timesyncd service should be enabled'
    assert service.is_running, 'systemd-timesyncd service should be started'


# ---
# timezone assertions:

def test_timezone(host, AnsibleDefaults):
    time_timezone = AnsibleDefaults.get('time_timezone')

    assert time_timezone is not None

    if not time_timezone:
        pytest.skip("time_timezone variable not set")

    current_timezone = host.file('/etc/timezone').content_string.strip()
    localtime = host.file('/etc/localtime')

    # /etc/timezone should match desired timezone
    assert current_timezone == time_timezone, \
        f'/etc/timezone should be {time_timezone}'

    # /etc/localtime should be symlink to correct zoneinfo file
    assert localtime.is_symlink, '/etc/localtime should be a symlink'
    assert localtime.linked_to == f'/usr/share/zoneinfo/{time_timezone}'


# ---
# RTC assertions:

# Check for hwclock binary presence
def test_hwclock_command(host, AnsibleDefaults):
    if not AnsibleDefaults.get('time_set_rtc'):
        command = host.exists('hwclock')
        assert command, 'hwclock binary should be available'
    else:
        pytest.skip('Skipping RTC file check: \'time_set_rtc\' is not enabled')


# Ensure rtc module config file exists and is correctly set when RTC is enabled
def test_rtc_module_load_file(host, AnsibleDefaults):
    if not AnsibleDefaults.get('time_set_rtc'):
        file = host.file('/etc/modules-load.d/rtc.conf')

        assert file.exists, \
            '/etc/modules-load.d/rtc.conf must exist'
        assert file.content_string.strip() == 'rtc', \
            'rtc.conf content must be \'rtc\''

        assert file.user == 'root'
        assert file.group == 'root'
        assert file.mode == 0o644
    else:
        pytest.skip('Skipping RTC file check: \'time_set_rtc\' is not enabled')


# ---
# timedatectl assertions:

# Confirm that NTP is enabled via the timedatectl command
def test_timedatectl_ntp_enabled(host):
    cmd = host.run('timedatectl show -p NTP --value')
    assert cmd.stdout.strip() == 'yes', 'NTP should be enabled via timedatectl'
