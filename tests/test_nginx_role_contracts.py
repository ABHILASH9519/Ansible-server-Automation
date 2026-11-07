from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_nginx_role_validates_inputs_before_installing_packages():
    tasks = yaml.safe_load(
        (ROOT / "roles/nginx_site/tasks/main.yml").read_text(encoding="utf-8")
    )

    assert tasks[0]["name"] == "Validate Nginx role inputs before changing the host"
    assert "ansible.builtin.assert" in tasks[0]
    conditions = tasks[0]["ansible.builtin.assert"]["that"]
    assert "nginx_listen_port | int >= 1" in conditions
    assert "nginx_listen_port | int <= 65535" in conditions
    assert "nginx_site_root is match('^/')" in conditions
    assert "nginx_server_name is match('^[A-Za-z0-9*._-]+$')" in conditions
    assert tasks[1]["name"] == "Install Nginx package"
