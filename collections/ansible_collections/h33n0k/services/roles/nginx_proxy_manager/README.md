# Nginx Proxy Manager

## Role Description

### What is Nginx Proxy Manager ?

Nginx Proxy Manager (NPM) is a lightweight, self-hosted reverse proxy solution with a clean and powerful web UI. Built on top of Nginx, it allows you to manage your reverse proxies, SSL certificates, and access control without needing to manually edit configuration files.

This role installs and configures NPM inside a Docker container using the unofficial [`jlesage/nginx-proxy-manager`](https://hub.docker.com/r/jlesage/nginx-proxy-manager) image, and leverages the `h33n0k.tools.docker` role to manage Docker installation.

- Web-based UI for reverse proxy configuration
- Automatic SSL via Let's Encrypt
- Access control and authentication
- Custom redirects, streams, and headers
- Multi-domain support
- Built-in REST API

### Use Cases

- Securely expose internal web services (e.g. Nextcloud, Home Assistant)
- Manage and auto-renew Let's Encrypt certificates
- Centralize proxy and firewall rules via a UI
- Manage reverse proxy hosts programmatically (unofficial API)
- Simplify multi-domain setups on a single public IP

## Role Features

- Deploys `jlesage/nginx-proxy-manager` Docker container
- Mounts two volumes following Linux Filesystem Hierarchy Standards:
```yaml
- "/var/log/nginx‑proxy‑manager:/config/logs:rw"
- "/etc/opt/nginx‑proxy‑manager:/config:rw"
```
- Initializes NPM with custom admin credentials by replacing the default admin@example.com
- Supports secure user management via `nginx_proxy_manager_users` variable

## Requirements
- Ansible >= 2.12
- Linux host with Docker
- Dependent role: h33n0k.tools.docker

## Role Variables

### Container Configuration

| Variable                               | Default                             | Description                                     |
| -------------------------------------- | ----------------------------------- | ----------------------------------------------- |
| `nginx_proxy_manager_name`             | `nginx-proxy-manager`               | Name of the Docker container                    |
| `nginx_proxy_manager_image`            | `jlesage/nginx-proxy-manager`       | Docker image used for NPM                       |
| `nginx_proxy_manager_restart`          | `unless-stopped`                    | Restart policy for the container                |
| `nginx_proxy_manager_external_network` | `nginx-proxy`                       | Docker external network to attach the container |
| `nginx_proxy_manager_ports`            | `['80:8080', '81:8181', '443:443']` | List of port mappings (host\:container)         |

### Default Admin User

| Variable                               | Default             | Description                                 |
| -------------------------------------- | ------------------- | ------------------------------------------- |
| `nginx_proxy_manager_default_email`    | `admin@example.com` | Default admin email used at first launch    |
| `nginx_proxy_manager_default_password` | `changeme`          | Default admin password used at first launch |

### Service Setup

| Variable                                        | Default | Description                                                                                         |
| ----------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------- |
| `nginx_proxy_manager_setup`                     | `false` | Whether to setup and deploy the NPM container                                                       |
| `nginx_proxy_manager_setup_users`               | `true`  | Whether to create or update user accounts                                                           |
| `nginx_proxy_manager_setup_update_default_user` | `true`  | Whether to replace the default admin@example.com with the first user in `nginx_proxy_manager_users` |

#### User Definitions

```yaml
nginx_proxy_manager_users:
  - name: 'John Doe'
    nickname: 'superadmin'
    email: 'johndoe@gmail.com'
    roles:
      - admin
    password: 'mysuperpassword'
```

Each user requires:

* `name` (Full name)
* `nickname` (Username)
* `email` (Unique address)
* `roles` (`[admin]` or undefined)
* `password` (Clear text password)

> 🔐 Store credentials in a vaulted file (e.g. group_vars/all/vault.yml) using ansible-vault for production deployments.

## Example Playbook
```yaml
---
- name: Setup NGINX PROXY MANAGER
  hosts: all
  become: true
  collections:
    - h33n0k.services
  roles:
    - name: h33n0k.services.nginx_proxy_manager
      nginx_proxy_manager_setup: true
      nginx_proxy_manager_setup_users: true
      nginx_proxy_manager_setup_update_default_user: true
      nginx_proxy_manager_users:
        - name: 'John Doe'
          nickname: 'superadmin'
          email: 'johndoe@gmail.com'
          roles:
            - admin
          password: 'mysuperpassword'
```

## Notes on API Usage
The NPM UI runs on top of an internal REST API, though it is not officially documented.
You may inspect requests using `http://localhost:81/api/schema` endpoint.
> ⚠️ Use caution when scripting API access. Upgrades may break unofficial integrations.

## Author

[@h33n0k](https://github.com/h33n0k) — DevOps & Software Engineer
