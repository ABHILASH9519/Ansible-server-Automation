# Deployment checklist

- [ ] Use a disposable Linux VM for first execution.
- [ ] Confirm SSH connectivity and privilege escalation.
- [ ] Review `group_vars/all.yml`, package names, port, and server name.
- [ ] Confirm the chosen port is allowed by the host firewall and cloud security group.
- [ ] Run `ansible-playbook -i inventories/production/hosts.yml playbooks/site.yml --syntax-check`.
- [ ] Run the playbook first with `--check --diff` where supported.
- [ ] Back up any existing Nginx configuration before rollout.
- [ ] Run `playbooks/validate.yml` and verify `/healthz` from the intended network.
- [ ] Keep secrets in a secret manager or Ansible Vault; never commit credentials.
- [ ] Define rollback steps before production changes.
