# 📄 Syslog Protocol

The Syslog protocol defines a standard for message logging in Unix-like systems. It is used by various system components and services to emit log messages in a structured and transportable format.

This document provides a high-level overview of how the syslog protocol works, its structure, and its role in log management on Debian systems.

---

# 🧱 Syslog Message Structure

Syslog messages follow a well-defined structure standardized in [RFC 5424](https://datatracker.ietf.org/doc/html/rfc5424). A typical syslog message contains:

```text
<PRI>VERSION TIMESTAMP HOSTNAME APP-NAME PROCID MSGID [STRUCTURED-DATA] MSG
```

### Key Components

- **`<PRI>`** – Priority value derived from facility and severity.
- **`VERSION`** – Syslog protocol version (e.g., `1` for RFC 5424).
- **`TIMESTAMP`** – ISO 8601 or RFC 3339 timestamp.
- **`HOSTNAME`** – System hostname that sent the log.
- **`APP-NAME`** – Name of the application emitting the message.
- **`PROCID`** – Process ID or `-` if not applicable.
- **`MSGID`** – Identifier for the type of message.
- **`STRUCTURED-DATA`** – Optional JSON-like metadata fields.
- **`MSG`** – The actual log message content.

Example:

```text
<34>1 2025-04-24T14:10:00Z web01 nginx 1234 ID47 - Client connected from 192.168.1.42
```

---

# 🎚️ Priority (`PRI`) Value

The priority (`PRI`) is a numerical value combining **facility** and **severity**:

```text
PRI = (Facility × 8) + Severity
```

### Facility Examples

| Code | Facility         |
|------|------------------|
| 0    | kernel messages  |
| 1    | user-level       |
| 3    | system daemons   |
| 10   | security/authorization |

### Severity Levels

| Code | Severity          |
|------|-------------------|
| 0    | Emergency         |
| 1    | Alert             |
| 2    | Critical          |
| 3    | Error             |
| 4    | Warning           |
| 5    | Notice            |
| 6    | Informational     |
| 7    | Debug             |

You can filter logs in `rsyslog` using these levels:

```text
*.info;mail.none;authpriv.none;cron.none    /var/log/messages
```

---

# 🌐 Transport Mechanisms

Syslog supports several transport methods:

- **Unix domain sockets** (default on local systems):  
  `/dev/log`
- **UDP 514** (legacy, unreliable)
- **TCP 514** (reliable, supports TLS)
- **TLS (RFC 5425)** for encrypted and authenticated log forwarding

Example of forwarding via TCP:

```conf
*.* @@logserver.example.com:514
```

The `@` prefix means UDP, `@@` means TCP.

---

# 🛡️ Security & Best Practices

- Prefer **TLS over TCP** for sending logs across untrusted networks.
- Limit and rate-limit incoming log traffic to mitigate flooding or denial of service. (e.g fail2ban)
- Separate high-verbosity logs (e.g., debug) from critical infrastructure logs.

---

# 🔍 See also

- [rsyslog Documentation](https://www.rsyslog.com/doc/)
- [RFC 5424 - Syslog Protocol](https://datatracker.ietf.org/doc/html/rfc5424)
