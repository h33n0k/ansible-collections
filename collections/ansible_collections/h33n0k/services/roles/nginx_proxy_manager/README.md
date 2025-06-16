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
- Supports Users management
- Supports Access Lists management

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

## Tasks Usage

### User Configuration

#### Update User:
Update Default User:

```yaml
- name: Update Default User
  ansible.builtin.include_role:
    name: h33n0k.services.nginx_proxy_manager
    tasks_from: user/update
  vars:
    user:
      id: 1
      name: 'John Doe'
      nickname: 'superadmin'
      email: 'johndoe@gmail.com'
      roles:
        - admin
      password:
        current: changeme
        new: 'mysuperpassword'
```

### Access Lists Configuration

#### Create ACL:
```yaml
- name: Set Admin Access
  ansible.builtin.include_role:
    name: h33n0k.services.nginx_proxy_manager
    tasks_from: access_lists/set
  vars:
    list:
      name: Admin
      satisfy_any: true # Default (true)
      pass_auth: false # Default (false)
      users:
        - username: johndoe
          password: mysuperpassword
      access:
        - address: 0.0.0.0/0
          directive: allow
```

> 🔐 Store credentials in a vaulted file (e.g. group_vars/all/secrets.yml) using ansible-vault for production deployments.

## Example Playbook
[./playbooks/nginx-proxy-manager.yml](/playbooks/nginx-proxy-manager.yml)

## Notes on API Usage
The NPM UI runs on top of an internal REST API, though it is not officially documented.
You may inspect requests using `http://localhost:81/api/schema` endpoint.
> ⚠️ Use caution when scripting API access. Upgrades may break unofficial integrations.

## Author

[@h33n0k](https://github.com/h33n0k) — DevOps & Software Engineer
