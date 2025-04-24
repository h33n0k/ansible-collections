# 🔐 Audit Framework (`auditd`)

The Linux Audit Daemon (`auditd`) is a powerful subsystem designed to track and record security-relevant events on a Linux system. It provides detailed logs of system calls, file accesses, user authentication attempts, and policy rule violations.

This document outlines the purpose, configuration, and usage of `auditd` on Debian-based systems.

---

# 🎯 Purpose of `auditd`

The primary goal of `auditd` is to provide tamper-resistant logs of critical system activity. It is often required in high-security environments and is commonly used for:

- Security incident detection and response
- Compliance with standards (e.g., [PCI-DSS](https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard), [HIPAA](https://en.wikipedia.org/wiki/Health_Insurance_Portability_and_Accountability_Act), [NIST](https://en.wikipedia.org/wiki/National_Institute_of_Standards_and_Technology))
- Forensic investigation
- User accountability and monitoring

---

# ⚙️ Components of the Audit System

### `auditd`

The main daemon that writes audit records to disk.

### `auditctl`

Command-line tool to define or inspect rules at runtime.

### `ausearch` / `aureport`

Tools for querying and generating human-readable reports from the audit logs.

---

# 🛠️ Configuration

## Runtime Rules (Volatile)

Set with `auditctl`, lost on reboot:

```bash
auditctl -a always,exit -F arch=b64 -S execve -k exec_log
```

## Persistent Rules (Recommended)

Define rules in:

```bash
/etc/audit/rules.d/*.rules
```

These are compiled at boot into:

```bash
/etc/audit/audit.rules
```

Example persistent rule:

```bash
-w /etc/passwd -p wa -k identity_changes
```

This watches `/etc/passwd` for writes and attribute changes.

---

# 📂 Log Files

Audit logs are stored in:

```bash
/var/log/audit/audit.log
```

These logs are structured but can be queried with audit tools for readability.

---

# 📊 Querying Logs

Search for entries by key:

```bash
ausearch -k exec_log
```

Search by user ID:

```bash
ausearch -ua 1000
```

Generate a report:

```bash
aureport --summary
```

---

# 📏 Best Practices

- 🧱 Use **structured rules** with `-k` tags for easy filtering.
- 🔒 Store logs on **read-only or external media** for critical systems.
- 🧑‍💼 Use **central log collection** with tools like rsyslog or remote audit logging.
- 🔁 Rotate audit logs regularly (see logrotate integration).

---

# 🚨 Example Use Cases

| Use Case                  | Rule Example                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| Track `sudo` usage        | `-w /usr/bin/sudo -p x -k sudo_activity`                                     |
| Monitor user home access  | `-w /home -p rwa -k home_access`                                             |
| Record executed commands  | `-a always,exit -F arch=b64 -S execve -k exec_tracking`                      |
| Detect passwd modification| `-w /etc/passwd -p wa -k passwd_changes`                                     |

---

# 🔍 See also

- [auditd Documentation](https://github.com/linux-audit/audit-documentation)
