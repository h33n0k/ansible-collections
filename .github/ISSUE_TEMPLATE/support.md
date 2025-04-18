---
name: 🙋 Support Request
about: Get help with using or understanding the project
labels: [support]
body:

  - type: markdown
    attributes:
      value: |
        Need support? Please describe your problem clearly and include any context that might help us assist you.

  - type: textarea
    id: problem
    attributes:
      label: What do you need help with?
      description: Describe your situation and what you're trying to do.
      placeholder: "I'm trying to use the docker role on a VPS, but it fails on the install step..."
    validations:
      required: true

  - type: textarea
    id: attempts
    attributes:
      label: What have you tried?
      description: Let us know what you've already attempted.
    validations:
      required: false

  - type: input
    id: environment
    attributes:
      label: Environment Info (optional)
      placeholder: "Debian 12 / Ansible 2.14.2"
---

# Need support? Please describe your problem clearly and include any context that might help us assist you.

## What do you need help with?
Describe your situation and what you're trying to do (e.g., "I can't get the `docker` role to work on my VPS setup...").

## What have you tried?
List what you've already attempted, such as commands or methods (e.g., "I tried installing Docker manually, but I still get an error...").

## Environment Info (optional)
Provide any relevant details about your environment:
- OS (e.g., Debian 12)
- Ansible version (e.g., 2.14.2)
- Any relevant versions of dependencies or tools (e.g., Docker version)
