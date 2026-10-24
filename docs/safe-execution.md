# Safe execution and rollback runbook

## Before changing a host
1. Confirm the inventory host list and the SSH identity that Ansible will use.
2. Confirm the host is in a supported Debian- or RedHat-family distribution.
3. Review `group_vars/all.yml` and any host-specific overrides.
4. Use a disposable VM first; ensure console access or a recovery path exists.
5. Run syntax checks, then a dry run where supported:

```bash
ansible-playbook -i inventories/production/hosts.yml.example playbooks/site.yml --syntax-check
ansible-playbook -i inventories/production/hosts.yml.example playbooks/site.yml --check --diff
```

The example inventory uses documentation-only addresses and is not a real target. Replace it with a protected local inventory before connecting to infrastructure.

## Apply and validate
- Start with one canary host using `--limit`.
- Review changed tasks before widening the rollout.
- Run `playbooks/validate.yml` after applying the configuration.
- Verify the Nginx health endpoint from a network that is expected to reach it.
- Check service status and logs before declaring the rollout healthy.

## Rollback
1. Stop the rollout; do not rerun blindly if a task fails partway through.
2. Restore the backed-up Nginx configuration and site content if they were overwritten.
3. Validate Nginx configuration before reloading it.
4. Restore prior package/configuration state using the host's approved recovery procedure.
5. Re-run validation and document the cause and recovery.

Ansible check mode is not a full simulation: some tasks and modules cannot predict every change. No production host has been configured by this repository's CI.
