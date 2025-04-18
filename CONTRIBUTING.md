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

---

## Tips

- Ensure your code is formatted and linted before committing.
