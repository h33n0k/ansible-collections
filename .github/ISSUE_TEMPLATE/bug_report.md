---
name: 🐞 Bug Report
about: File a bug report if something isn't working as expected
labels: [bug]
body:

  - type: markdown
    attributes:
      value: |
        Please fill out this form to help us debug the issue.

  - type: textarea
    id: summary
    attributes:
      label: Summary
      description: A clear and concise description of the issue.
      placeholder: "The `nginx` role fails when running on a minimal Debian 12 image..."
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce the bug?
      placeholder: |
        1. Use `inventory/test`
        2. Run `ansible-playbook playbooks/webserver.yml`
        3. See error message...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant Logs or Output
      description: Include the output of the command or task that failed.
      render: shell
      placeholder: |
        TASK [nginx : Install packages]
        failed: [debian01] => (item=nginx) => {"msg": "No package matching 'nginx' is available"}
    validations:
      required: false

  - type: input
    id: version
    attributes:
      label: Ansible Version
      placeholder: "ansible 2.14.2"
    validations:
      required: false

  - type: input
    id: os
    attributes:
      label: Target OS / Distro
      placeholder: "Debian 12 (bookworm)"
    validations:
      required: false
---

# Please fill out this form to help us debug the issue.

## Bug Summary
Provide a brief summary of the bug (e.g., "The `nginx` role fails on minimal Debian 12 setup").

## Steps to Reproduce
Please provide detailed steps on how to reproduce the issue:
1. Step one (e.g., "Use `inventory/test`").
2. Step two (e.g., "Run `ansible-playbook playbooks/webserver.yml`").
3. Step three (e.g., "See the error message...").

## Expected Behavior
What did you expect to happen? Be as clear and specific as possible.

## Logs or Output
Please include any relevant logs or output from the command or task that failed. For example:
```
TASK [nginx : Install packages]
failed: [debian01] => (item=nginx) => {"msg": "No package matching 'nginx' is available"}
```

## Ansible Version (optional)
Please provide the version of Ansible you are using, such as `ansible 2.14.2`.

## OS / Distro (optional)
Please specify the target OS and version (e.g., "Debian 12").
