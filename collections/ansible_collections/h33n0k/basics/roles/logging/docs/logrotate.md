# ♻️ Log Rotation with `logrotate`

`logrotate` is the standard tool on Debian-based systems for managing log file growth. It automates the process of compressing, archiving, and deleting logs to prevent disk space exhaustion and ensure long-term log availability.

This document outlines how `logrotate` works, how to configure it, and best practices for integrating it with other logging services like `rsyslog` and `auditd`.

---

# 📦 Why Log Rotation Matters

Without log rotation, log files can:

- Grow indefinitely and fill disk space
- Become difficult to parse or manage
- Pose a risk to system stability or compliance

Rotating logs ensures:

- Predictable disk usage
- Historical log retention
- Easier parsing and offloading

---

# 🛠️ How `logrotate` Works

`logrotate` runs periodically (typically via `cron` or `systemd`) and reads configuration files that define:

- Which logs to rotate
- When to rotate them (daily, weekly, monthly, etc.)
- How many old versions to keep
- Whether to compress, rename, or delete old logs
- Which post-rotation actions to run (e.g., service reloads)

The main configuration file is:

```bash
/etc/logrotate.conf
```

Additional per-service configs are stored in:

```bash
/etc/logrotate.d/
```

---

# ✍️ Configuration Example

Here’s an example configuration for `rsyslog`:

```conf
/var/log/syslog
{
    rotate 7
    daily
    missingok
    notifempty
    compress
    delaycompress
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
```

### Breakdown

- `rotate 7`: Keep 7 old logs
- `daily`: Rotate logs every day
- `missingok`: Don't error if file doesn't exist
- `notifempty`: Skip empty files
- `compress`: Gzip rotated logs
- `delaycompress`: Compress the log after the next rotation
- `postrotate/endscript`: Commands to run after rotation (e.g., signal `rsyslogd`)

---

# 🔁 Rotation for `auditd`

Audit logs have their own built-in rotation managed by:

```bash
/etc/audit/auditd.conf
```

Key options:

```ini
max_log_file = 100      # Max size in MB
num_logs = 10           # Number of rotated logs to keep
max_log_file_action = ROTATE
```

Do **not** rotate `/var/log/audit/audit.log` using `logrotate`, or it may interfere with `auditd`.

---

# 📌 Tips & Best Practices

- Use `delaycompress` to avoid compressing active logs.
- Monitor disk space usage with `du` or `ncdu`.
- Ensure services that write logs are notified or gracefully handle rotation.
- Use `copytruncate` only for apps that cannot reopen logs on `SIGHUP` (can cause data loss).

---

# 🔍 See also

- [`logrotate` manpage](https://man7.org/linux/man-pages/man8/logrotate.8.html)
