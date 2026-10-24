# Ansible Server Automation

A role-based Ansible project for repeatable Linux baseline configuration and a managed Nginx landing page.

## Status

Project structure and YAML regression tests are included in `tests/` and run in GitHub Actions alongside Ansible playbook syntax checks. A real deployment against a disposable Linux target is still pending.

## Structure

- `inventories/` — local and production inventory examples
- `playbooks/` — site configuration and validation playbooks
- `roles/` — baseline, operations-user, and Nginx site roles
- `docs/` — architecture and deployment checklist
- `.github/workflows/` — CI validation workflows

## Requirements

- Python 3.10+
- Ansible Core (install with `python -m pip install -r requirements.txt`)
- SSH access and privilege escalation for remote Linux hosts

## Run

Review the inventory and variables before running against any host. For a local syntax check:

```bash
ansible-playbook -i inventories/local/hosts.yml playbooks/site.yml --syntax-check
```

For remote hosts, configure SSH credentials securely and review `group_vars/all.yml`. Do not commit secrets or run against production without a maintenance plan.

## Tests and verification

Run the repository regression tests with:

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
```

Run Ansible syntax checks with:

```bash
ansible-playbook -i inventories/local/hosts.yml playbooks/site.yml --syntax-check
ansible-playbook -i inventories/local/hosts.yml playbooks/validate.yml --syntax-check
```

GitHub Actions runs both sets of checks on pushes and pull requests. Syntax checks do not prove that configuration will work on every target OS, and neither test suite is a substitute for a deployment rehearsal on a disposable Linux VM. Do that before production use.
