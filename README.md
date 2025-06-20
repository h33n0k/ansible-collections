# 🐧 Debian Playbooks

This repository contains a curated set of Ansible collections and roles tailored for provisioning, configuring, and managing Debian-based systems. It aims to streamline infrastructure management with a modular, reusable, and maintainable approach.

## ✅ Requirements

- **Ansible**: Version `2.12+` is required.
- **Target OS**: Debian 12

For installation instructions and platform-specific requirements, refer to the [official Ansible installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).

## 📘 Documentation

Each role is self-contained and documented following a consistent structure to improve readability and usage. In every role directory, you'll typically find:

- `README.md`: Role description, supported variables, and usage examples.
- `defaults/main.yml`: Default values for role variables.
- `meta/main.yml`: Metadata (platforms, dependencies).
- `examples/`: Sample playbooks for common use cases.

This structure promotes clarity and encourages reuse across projects.

## 🚀 Use Cases

### 🔧 Provisioning
- Bootstrap fresh Debian servers using the [`basics`](./collections/ansible_collections/h33n0k/basics/README.md) roles:
  - Timezone and locale setup
  - User and SSH configuration
  - System log and log rotation
  - System updates and package installation

### 🪚 Tool Setup
- Install and configure tools like:
    - Docker

### 🌐 Services Deployment
- Install and configure web servers (e.g., Nginx)
- Set up Docker-based container environments

### 🔐 Hardening
- Apply basic security policies (e.g., UFW, fail2ban)

## 🧪 Testing & Linting

Linting is enforced across all roles to ensure code quality and best practices. To run linting:

```bash
make lint
make test # test all roles
make test ROLE=basics/time # test specific role
make test CHANGED_SINCE=<commit-hash> # test changed role since this commit
```

---

## Roles Documentation
- Basics:
    - [Auth](./collections/ansible_collections/h33n0k/basics/roles/auth/README.md)
    - [Logging](./collections/ansible_collections/h33n0k/basics/roles/logging/README.md)
    - [Time](./collections/ansible_collections/h33n0k/basics/roles/time/README.md)
- Security:
    - [Firewall](./collections/ansible_collections/h33n0k/security/roles/firewall/README.md)
- Tools:
    - [Docker](./collections/ansible_collections/h33n0k/tools/roles/docker/README.md)
- Services:
    - [Nginx Proxy Manager](./collections/ansible_collections/h33n0k/services/roles/nginx_proxy_manager/README.md)

---

## 🔬 Contributing
We welcome contributions! To get started: [CONTRIBUTING](./CONTRIBUTING.md)

## ⚖️ License
This project is licensed under the [MIT License](./LICENSE).
