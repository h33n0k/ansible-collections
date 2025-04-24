# 📜 Role Features

This role ensures:

### 🧾 Logging with rsyslog
- Installation of `rsyslog`
- Deployment of custom `/etc/rsyslog.conf` from template
- Deployment of logrotate configuration in `/etc/logrotate.conf`
- Enabling and starting the `rsyslog` service

### 🛡️ Auditing with auditd
- Installation of `auditd` and `audispd-plugins`
- Deployment of a secure `/etc/audit/auditd.conf` from template
- Enabling and starting the `auditd` service
  - Service start is skipped during Molecule testing unless explicitly enabled

## 📘 Example Playbook

```yaml
---
- name: Configure system logging and auditing
  hosts: all
  roles:
    - h33n0ks.basics.logging
```

## ✅ Verification

### Check rsyslog status

```bash
systemctl status rsyslog
```

You should see:

```
Active: active (running)
```

You can also verify that logs are rotating correctly using:

```bash
cat /etc/logrotate.d/rsyslog.conf
```

### Check auditd status

```bash
systemctl status auditd
```

Expect:

```
Active: active (running)
```

You can confirm that rules are being enforced with:

```bash
auditctl -s
```

## 📝 Documentation

See the [docs/index.md](./docs/index.md) file for detailed documentation on templates, variables, and customization options.

## 🪪 License

This project is licensed under the [MIT License](./LICENSE).
