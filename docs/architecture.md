# Architecture

The `site.yml` playbook targets the `linux_servers` inventory group and applies three roles:

1. `base` installs a small baseline package set using the host's package manager.
2. `operations_user` creates an optional operations account only when explicitly enabled.
3. `nginx_site` installs Nginx, renders a static page and a managed server block, and ensures the service is enabled.

The Nginx site listens on `nginx_listen_port` (8080 by default) and exposes `/healthz` as a simple health endpoint. Review port exposure and firewall rules before deployment.

The default local inventory uses a local connection. It is intended for syntax and controlled local testing, not as proof that every task can safely run on a developer workstation.

## Role and configuration flow

```mermaid
flowchart TD
    Inv[Inventory: linux_servers] --> Vars[group_vars/all.yml]
    Inv --> Site[playbooks/site.yml]
    Vars --> Site
    Site --> Base[roles/base]
    Site --> Ops[roles/operations_user]
    Site --> Web[roles/nginx_site]
    Base --> Pkg[Baseline package state]
    Ops --> User[Optional operations account]
    Web --> Tpl[Template server block + page]
    Tpl --> Nginx[Nginx service enabled]
    Nginx --> Probe["GET /healthz :8080"]
```

## Validation and safe execution

```mermaid
flowchart LR
    Review[Review variables and inventory] --> Syntax[Ansible syntax check]
    Syntax --> Tests[pytest regression suite]
    Tests --> Check[Check mode + diff]
    Check --> Decision{Approved for test host?}
    Decision -- No --> Edit[Revise and rerun]
    Edit --> Syntax
    Decision -- Yes --> VM[Disposable Linux VM]
    VM --> Verify[Validate service and health endpoint]
```

## Role responsibilities

| Role | Responsibility |
|---|---|
| `base` | Baseline packages and supported operating-system checks |
| `operations_user` | Optional operations account controlled by explicit configuration |
| `nginx_site` | Nginx package, templated site configuration, service handler and health endpoint |

## Verification boundary

Automated tests and syntax checks do not prove a successful configuration on every Linux distribution. Validate against a disposable VM before using this project on a real host.
