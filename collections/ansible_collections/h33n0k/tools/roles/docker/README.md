# Docker

## Role Description

`h33n0k.tools.docker` is an Ansible role that ensures Docker is installed, configured, and ready to manage containers, bind volumes, and permissions across environments.

This role is ideal for orchestrating containerized services and maintaining Docker infrastructure **as code**, while enforcing consistent volume layout and permission models on the host.

### Features

- Installs Docker Engine and required dependencies
- Manages container lifecycle: create, update, remove
- Configures bind mounts and named volumes with ownership and access control
- Supports bridge and custom IPAM networking
- Declarative container definition with support for env vars, port mappings, labels, and restart policies
- Follows [Filesystem Hierarchy Standard (FHS)](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) for persistent system services

### Use Cases

- Deploy system services like **NGINX Proxy Manager**, **Docker Mail Server**, or **GitLab**
- Provision application containers using named volumes for isolation and simplicity
- Enforce pre-existing volume layout before running containers
- Automate creation and management of Docker bridge networks
- Standardize containerized workloads across multiple hosts

---

## Role Variables

### Container Configuration

```yaml
container:
    name: string                     # Required
    image: string                    # Required
    restart: string                  # Default: "unless-stopped"
    ports:                           # Optional
      - "80:8080"
    env:                             # Optional environment variables
      VAR_NAME: value
    volumes:                         # Optional volume list
      - host: /host/path
        container: /container/path
        type: directory              # or 'file'
        group: docker                # optional group ownership
        access: rw                   # rw or ro (optional)
    networks:                        # Optional list of networks
      - name: my-net
        driver: bridge
        ipam_config:
          - subnet: 192.168.10.0/24
````

### Volume Fields

| Field       | Required | Description                                   |
| ----------- | -------- | --------------------------------------------- |
| `host`      | Yes      | Path on host system                           |
| `container` | Yes      | Path inside the container                     |
| `type`      | Yes      | `directory` or `file`                         |
| `group`     | No       | Group name or ID to assign (defaults to root) |
| `access`    | No       | `rw` (default) or `ro`                        |

### Example: System Service with Bind Mounts

```yaml
- name: Setup NGINX Proxy Manager
  ansible.builtin.include_role:
    name: h33n0k.tools.docker
    tasks_from: run
  vars:
    container:
      name: nginx-proxy-manager
      image: jc21/nginx-proxy-manager
      restart: unless-stopped
      ports:
        - "80:8080"
        - "81:8181"
        - "443:4443"
      env:
        USER_ID: "0"
        GROUP_ID: "4"
      volumes:
        - host: "/var/log/nginx-proxy-manager"
          container: "/config/logs"
          type: directory
          group: adm
        - host: "/etc/opt/nginx-proxy-manager"
          container: "/config"
          type: directory
      networks:
        - name: nginx-proxy
          driver: bridge
          ipam_config:
            - subnet: 192.168.10.0/24
```

---

## Storage Strategy: Named Volumes vs Bind Mounts

This role supports both **bind mounts** and **~~named volumes~~**, based on container purpose. This promotes consistency with systemd-like services and provides flexibility for apps requiring encapsulation.

### 🔧 Bind Mounts — System-Level Services

System services (e.g., **reverse proxy**, **GitLab**, **DMS**) are integrated with the host via bind mounts. These are placed under FHS-compliant directories, such as:

* `/etc/opt/<service>` — configuration
* `/var/opt/<service>` — data
* `/var/log/<service>` — logs
* `/var/lib/<service>` — state

**Why Bind Mounts?**

* Allows inspection and manipulation outside Docker
* Integrates with host backup, monitoring, and audit tooling
* Aligns with Unix system management practices

#### Example:

```yaml
volumes:
  - /etc/opt/gitlab:/etc/gitlab
  - /var/opt/gitlab:/var/opt/gitlab
  - /var/log/gitlab:/var/log/gitlab
```

---

### 📦 Named Volumes — Hosted Applications
> Currently not implemented.

Hosted applications (e.g., websites, SaaS clients) are deployed using **named volumes**, ideal for transient or isolated application state.

**Why Named Volumes?**

* Keeps host filesystem clean and abstracted
* Great for CI/CD automation and dynamic deployment
* Simplifies orchestration tools like Docker Compose or Swarm

#### Example:

```yaml
volumes:
  - my_webapp_data:/app/data
  - my_webapp_cache:/app/cache
```

---

## Summary

| Container Type      | Storage Method | Description                                    |
| ------------------- | -------------- | ---------------------------------------------- |
| System Services     | Bind Mounts    | Host-visible, FHS-compliant, backup-friendly   |
| Hosted Applications | Named Volumes  | Encapsulated, portable, ephemeral/app-specific |

This separation reinforces best practices: treat infrastructure as part of the host, and applications as disposable artifacts.

---

## Author

[@h33n0k](https://github.com/h33n0k) — DevOps & Software Engineer
