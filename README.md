# Ansible Server Automation

A role-based Ansible project for repeatable Linux baseline configuration and a managed Nginx landing page.

## Status

Initial repository sync. Automated structure tests and YAML parsing have been performed locally; Ansible runtime validation on a Linux target is still pending.

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

## Verification caveat

A successful YAML parse is not equivalent to an Ansible syntax check or a successful server deployment. Those checks must be run in an Ansible-enabled environment against a disposable Linux VM before production use.
