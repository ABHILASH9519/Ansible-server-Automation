from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_documentation_and_workflow_include_safe_execution_guidance():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    runbook = (ROOT / "docs/safe-execution.md").read_text(encoding="utf-8")
    workflow = (ROOT / ".github/workflows/ansible-checks.yml").read_text(encoding="utf-8")
    assert "disposable Linux target" in readme
    assert "--check --diff" in runbook
    assert "pull_request" in workflow


def test_no_real_production_hosts_or_credentials_in_example_inventory():
    inventory = yaml.safe_load(
        (ROOT / "inventories/production/hosts.yml.example").read_text(encoding="utf-8")
    )
    hosts = inventory["all"]["children"]["linux_servers"]["hosts"]
    assert list(hosts) == ["web01.example.internal"]
    assert hosts["web01.example.internal"]["ansible_host"] == "192.0.2.10"
    assert "ansible_password" not in str(inventory)
