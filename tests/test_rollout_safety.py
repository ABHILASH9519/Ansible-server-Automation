from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_site_playbook_uses_serial_fail_fast_rollout():
    playbook = yaml.safe_load(
        (ROOT / "playbooks/site.yml").read_text(encoding="utf-8")
    )

    assert len(playbook) == 1
    assert playbook[0]["serial"] == 1
    assert playbook[0]["any_errors_fatal"] is True
    assert playbook[0]["hosts"] == "linux_servers"
