# 📚 Logging Role Documentation

This directory contains the documentation for the Ansible `logging` role. This role ensures that logs on Debian-based systems are consistently collected, audited, rotated, and stored in a secure and structured manner.

Reliable logging is essential for system observability, security auditing, debugging, and compliance. This role automates the configuration of the core Linux logging stack: `rsyslog` for log transport and formatting, `auditd` for security auditing, and `logrotate` for controlled log file rotation and retention.

---

# 🧭 Importance of System Logging

Logging is the backbone of monitoring, troubleshooting, and security in any infrastructure.

## Why Proper Logging Matters

- **🔍 Debugging & Troubleshooting**  
  Logs offer the first clues when something goes wrong. Without complete and structured logs, root cause analysis becomes guesswork.

- **🔐 Security Auditing**  
  Logs are essential for detecting and responding to suspicious behavior, enforcing accountability, and complying with security policies.

- **📦 Disk Space Management**  
  Uncontrolled log growth can fill up disks. Proper rotation and retention strategies ensure system stability.

- **🛡️ Compliance**  
  Regulations like [PCI-DSS](https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard), [HIPAA](https://en.wikipedia.org/wiki/Health_Insurance_Portability_and_Accountability_Act), and [GDPR](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation) often require comprehensive log collection and retention.

- **📊 Monitoring & Alerting**  
  Logs feed observability stacks (e.g., ELK, Loki) to trigger alerts and generate dashboards.

---

# ⚙️ Logging on Debian Systems

## `rsyslog` – The Syslog Daemon

`rsyslog` is the default syslog implementation on Debian. It handles system and application logs, and can forward logs over the network.

### Benefits

- ✔️ Flexible and extensible via modules
- ✔️ Can write to local files or remote log servers
- ✔️ Supports structured logging ([RFC 5424](https://datatracker.ietf.org/doc/html/rfc5424)/JSON)

### Configuration

Main configuration file:

```bash
/etc/rsyslog.conf
```

Additional configuration directory:

```bash
/etc/rsyslog.d/
```

Restart to apply changes:

```bash
sudo systemctl restart rsyslog
```

Example: forwarding logs to a remote server

```bash
*.* @logserver.example.com:514
```

## `auditd` – Linux Audit Daemon

`auditd` records detailed logs of security-relevant events, including syscalls and file access patterns.

### Benefits

- ✔️ Mandatory for hardened or compliance-focused environments
- ✔️ Captures user actions, permission denials, and system changes
- ✔️ Supports fine-grained rule sets

### Configuration

Audit rules can be defined in:

```bash
/etc/audit/audit.rules
```

Or persistently via:

```bash
/etc/audit/rules.d/*.rules
```

Restart the audit daemon:

```bash
sudo systemctl restart auditd
```

To inspect logs:

```bash
ausearch
```

Or live monitoring:

```bash
auditctl -l
```

## `logrotate` – Log File Rotation

`logrotate` manages the size and retention of log files to prevent disk space issues.

### Benefits

- ✔️ Automated rotation, compression, and deletion
- ✔️ Easily configurable per service
- ✔️ Prevents log flooding and disk overfill

### Configuration

Global settings:

```bash
/etc/logrotate.conf
```

Per-package and custom rules:

```bash
/etc/logrotate.d/
```

Force rotation for testing:

```bash
sudo logrotate -f /etc/logrotate.conf
```

Example configuration for `/var/log/syslog`:

```conf
/var/log/syslog {
  daily
  missingok
  rotate 7
  compress
  delaycompress
  notifempty
  create 640 syslog adm
  postrotate
    /usr/lib/rsyslog/rsyslog-rotate
  endscript
}
```

---

# 🔍 See also

- [Syslog Protocol](./syslog.md)
- [Audit Framework](./auditd.md)
- [Log Rotation Strategy](./logrotate.md)
