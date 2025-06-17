# Contributing Guide

Thank you for considering contributing to this project! Follow the steps below to set up your development environment and start contributing.

---

## Requirements

- Python 3.11
- [Make](https://www.gnu.org/software/make/) (for running setup tasks)

---

## Setup Instructions

1. **Create the virtual environment**  
   This will create a `venv` directory and set up Python.

   ```bash
   make init
   ```

2. **Activate the virtual environment**

   ```bash
   source venv/bin/activate
   ```

3. **Install development dependencies**

   ```bash
   make prepare
   ```

3. **Test roles**
    
   ```bash
   make test # test all roles
   make test ROLE=basics/time # test specific role
   make test ROLE=tools/docker SCENARIO=volume COMMAND=converge
   make test STAGED_ONLY # test modified role
   make test CHANGED_SINCE=<commit-hash> # test changed role since this commit
   ```

---

## Tips

- Ensure your code is formatted, linted and tested before committing.
