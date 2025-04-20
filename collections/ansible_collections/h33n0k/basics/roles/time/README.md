# 🧰 Role Features

This role ensures:

- Installation and configuration of `systemd-timesyncd` or an alternative time daemon
- Correct timezone setting using `timedatectl`
- Enabling and starting relevant services
- Monitoring and validation of sync status
- Optional configuration of custom NTP servers

## Role Variables
Available variables are listed below (see `defaults/main.yml` for full list and default values):

```yaml
---
# NTP:
# Preferred NTP servers (queried first).
# These should be reliable and geographically close.
time_timesyncd_ntp_servers:
  - primary-ntp-1.example.com
  - primary-ntp-2.example.com

# FallbackNTP:
# Fallback NTP servers (used if primary servers are unavailable).
time_timesyncd_fallback_ntp_servers:
  - fallback-ntp-1.example.com
  - fallback-ntp-2.example.com

# PollIntervalMinSec:
# Maximum poll interval in seconds.
# Increased over time when synchronization is stable.
time_timesyncd_poll_min: seconds_as_number

# PollIntervalMaxSec:
# Maximum interval (in seconds) between NTP polls.
# Increases automatically when time appears stable.
time_timesyncd_poll_max: seconds_as_number

# RootDistanceMaxSec:
# Maximum root distance (in seconds) before an NTP server is considered invalid.
# Lower values enforce stricter time accuracy.
time_timesyncd_root_distance_max: seconds_as_number

# ConnectionRetrySec:
# Time (in seconds) to wait before retrying a failed NTP connection.
# Lower values enable quicker failover to other servers.
time_timesyncd_connection_rety: seconds_as_number

# SaveIntervalSec:
# Interval (in seconds) at which the synchronization state is persisted to disk.
# Lower values improve recovery after reboots; higher values reduce disk writes.
time_timesyncd_save_interval: seconds_as_number

# Timezone:
# Timezone to apply to the system (must match a valid entry in /usr/share/zoneinfo).
time_timezone: Region/City_or_Valid_Timezone
```

## Example Playbook
```yaml
---
- name: Configure system time
  hosts: all
  roles:
    - h33n0ks.basics.time
```

# ✅ Verification

After applying this role, you can verify time synchronization with:

```bash
timedatectl status
```

Check for lines like:

```
System clock synchronized: yes
NTP service: active
```

And review logs using:

```bash
journalctl -u systemd-timesyncd
```

## Documentation
Refer to [docs/index.md](./docs/index.md) for detailed documentation.

## License
This project is licensed under the [MIT License](./LICENSE).
