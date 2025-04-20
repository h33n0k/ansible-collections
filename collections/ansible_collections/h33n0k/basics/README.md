# basics

This Ansible collection provides roles to configure the time synchronization on Debian servers. It is designed to ensure your systems are properly synchronized with NTP and timezone is properly configured according to best practices.

## Collection Structure

The `basics` collection includes the following roles:

### 1. `time`
The `time` role ensures that your Debian server is configured for accurate time synchronization. It includes tasks for:

- Configuring NTP with `systemd-timesyncd` to synchronize system time.
- Managing and configuring the system's time zone.
- Configuring and managing the Real-Time Clock (RTC) device.
  
By using this role, you ensure that the server is synchronized with accurate time sources, minimizing issues caused by time discrepancies.

For detailed documentation of the `time` role, refer to [time/README.md](./roles/time/README.md).

#### Key Variables:
```yaml
time_timesyncd_ntp_servers: []          # List of NTP servers to synchronize with
time_timesyncd_fallback_ntp_servers: [] # List of fallback NTP servers
time_timesyncd_poll_min: 32             # Minimum polling interval (seconds)
time_timesyncd_poll_max: 1024²          # Maximum polling interval (seconds)
time_timesyncd_root_distance_max: 0.1   # Maximum time drift allowed (seconds)
time_timesyncd_connection_retries: 5    # Number of connection retries
time_timesyncd_save_interval: 3600      # Interval for saving the system time to the RTC
time_timezone: 'Etc/UTC'                # Time zone to configure
time_rtc_device: '/dev/rtc0'            # Path to the RTC device
time_rtc_module: 'rtc_cmos'             # RTC module to load (e.g., rtc_cmos)
```

## Role Usage

To use the `basics` collection in your playbooks, simply include the roles as shown below:

```yaml
---
- name: Configure Time
  hosts: all
  collections:
    - h33n0k.basics
    roles:
    - h33n0k.basics.time
```

## Requirements

- Ansible 2.12 or higher.
- Supported for Debian-based systems (Debian 9 and later).

## License
This project is licensed under the [MIT License](./LICENSE).
