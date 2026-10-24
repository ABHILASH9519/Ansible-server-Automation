from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path):
    with (ROOT / relative_path).open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def test_site_playbook_targets_linux_servers_and_declares_roles():
    playbook = load_yaml("playbooks/site.yml")
    assert isinstance(playbook, list) and len(playbook) == 1
    assert playbook[0]["hosts"] == "linux_servers"
    assert playbook[0]["become"] is True
    assert playbook[0]["roles"] == ["base", "operations_user", "nginx_site"]


def test_validation_playbook_has_a_task_list():
    playbook = load_yaml("playbooks/validate.yml")
    assert isinstance(playbook, list) and len(playbook) == 1
    assert isinstance(playbook[0].get("tasks"), list)
    assert playbook[0]["tasks"]


def test_role_task_and_handler_files_are_valid_yaml_lists():
    paths = [
        "roles/base/tasks/main.yml",
        "roles/operations_user/tasks/main.yml",
        "roles/nginx_site/tasks/main.yml",
        "roles/nginx_site/handlers/main.yml",
    ]
    for path in paths:
        document = load_yaml(path)
        assert isinstance(document, list), f"{path} must contain a YAML list"
        assert document, f"{path} must not be empty"


def test_nginx_template_and_workflow_files_exist():
    required = [
        "roles/nginx_site/templates/index.html.j2",
        "roles/nginx_site/templates/site.conf.j2",
        ".github/workflows/ansible-checks.yml",
    ]
    for path in required:
        assert (ROOT / path).is_file(), f"Missing required file: {path}"


def test_defaults_keep_optional_user_creation_disabled_and_use_expected_port():
    defaults = load_yaml("group_vars/all.yml")
    assert defaults["create_operations_user"] is False
    assert defaults["nginx_listen_port"] == 8080
    assert defaults["nginx_site_root"] == "/var/www/ansible-managed-site"


def test_nginx_health_endpoint_and_handlers_are_wired():
    template = (ROOT / "roles/nginx_site/templates/site.conf.j2").read_text(encoding="utf-8")
    handlers = load_yaml("roles/nginx_site/handlers/main.yml")
    assert "location = /healthz" in template
    assert 'return 200 "ok\\n";' in template
    names = {handler["name"] for handler in handlers}
    assert "Validate and reload Nginx" in names
    assert "Reload Nginx" in names
    validate_handler = next(h for h in handlers if h["name"] == "Validate and reload Nginx")
    assert validate_handler["notify"] == "Reload Nginx"


def test_production_inventory_is_an_example_not_a_real_target():
    inventory = load_yaml("inventories/production/hosts.yml.example")
    hosts = inventory["all"]["children"]["linux_servers"]["hosts"]
    assert list(hosts) == ["web01.example.internal"]
    assert hosts["web01.example.internal"]["ansible_host"] == "192.0.2.10"
