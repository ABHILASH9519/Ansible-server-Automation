<div align="center">

# ⚙️ Ansible Server Automation

**Repeatable Linux baseline configuration and managed Nginx deployment with Ansible roles**

[![Ansible Checks](https://github.com/ABHILASH9519/Ansible-server-Automation/actions/workflows/ansible-checks.yml/badge.svg)](https://github.com/ABHILASH9519/Ansible-server-Automation/actions/workflows/ansible-checks.yml)
![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?logo=ansible&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Configuration-FCC624?logo=linux&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-Web%20Server-009639?logo=nginx&logoColor=white)
![Testing](https://img.shields.io/badge/Tests-Pytest%20%2B%20Syntax%20Checks-2E8B57)

[Architecture](#-architecture) · [Workflow](#-configuration-workflow) · [Quick start](#-local-checks) · [Safe execution](#-safe-first-run)

</div>

---

A role-based Ansible project for repeatable Linux baseline configuration and a managed Nginx landing page.

## ✨ Capabilities

- Reusable roles for base packages, optional operations user and Nginx site configuration
- Inventory-driven target selection and shared defaults
- Managed templates and handlers for configuration changes
- Health endpoint at `/healthz` on port 8080 by default
- Automated regression tests and Ansible syntax validation in GitHub Actions
- Documented check-mode, rollout and rollback practices

## 🧭 Architecture

```mermaid
flowchart TD
    Operator[Operator / CI] --> Inventory[Inventory + group_vars]
    Inventory --> Playbook[playbooks/site.yml]
    Playbook --> Base[base role]
    Playbook --> Ops[operations_user role<br/>opt-in]
    Playbook --> Nginx[nginx_site role]
    Base --> Packages[Baseline packages]
    Ops --> Account[Operations account]
    Nginx --> Template[Managed config + HTML template]
    Template --> Service[Nginx service]
    Service --> Health["/healthz :8080"]
    Tests[pytest + Ansible syntax checks] -. validates structure .-> Playbook
    style Playbook fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A
    style Nginx fill:#DCFCE7,stroke:#16A34A,color:#14532D
    style Tests fill:#F3E8FF,stroke:#9333EA,color:#581C87
```

## 🔄 Configuration workflow

```mermaid
flowchart LR
    A[Review inventory and variables] --> B[Run syntax checks]
    B --> C[Run pytest]
    C --> D[Use check mode and diff]
    D --> E{Change reviewed?}
    E -- No --> F[Revise configuration]
    F --> B
    E -- Yes --> G[Apply to disposable test VM]
    G --> H[Validate service and health endpoint]
    H --> I[Record outcome / rollback if needed]
    style E fill:#FEF3C7,stroke:#D97706,color:#78350F
    style G fill:#DCFCE7,stroke:#16A34A,color:#14532D
```

## 📊 Status and verification

The repository includes regression tests, YAML/playbook syntax checks and a documented safe-execution procedure. CI does **not** connect to or configure a real Linux host; a disposable-VM integration run remains a separate validation step.

## 🗂️ Project layout

- `inventories/` — local inventory and documentation-only production example
- `playbooks/site.yml` — applies the baseline, optional operations user and Nginx site roles
- `playbooks/validate.yml` — checks the resulting host configuration
- `roles/` — reusable Ansible roles
- `group_vars/all.yml` — shared defaults
- `tests/` — regression tests for structure, defaults, handlers and safe-execution docs
- `docs/` — architecture, deployment checklist and safe-execution/rollback runbook
- `.github/workflows/ansible-checks.yml` — CI tests and syntax checks

## 🧰 Requirements

- Python 3.10+
- Ansible Core and dependencies from `requirements.txt`
- SSH access and privilege escalation for remote Linux hosts

## ⚡ Local checks

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
ansible-playbook -i inventories/local/hosts.yml playbooks/site.yml --syntax-check
ansible-playbook -i inventories/local/hosts.yml playbooks/validate.yml --syntax-check
```

## 🛡️ Safe first run

Use a disposable VM and review all variables before connecting to any host. Start with syntax validation, then use check mode where supported:

```bash
ansible-playbook -i inventories/production/hosts.yml.example playbooks/site.yml --syntax-check
ansible-playbook -i inventories/production/hosts.yml.example playbooks/site.yml --check --diff
```

The example inventory intentionally uses documentation-only addresses. Replace it with your own protected inventory before attempting a real run. Check mode is not a perfect simulation for every module.

Read [the safe execution and rollback runbook](docs/safe-execution.md) before applying changes. Never commit passwords, private keys, vault passwords or production inventory secrets.
