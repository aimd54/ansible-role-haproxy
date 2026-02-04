"""Tests for HAProxy systemd override."""

OVERRIDE_DIR = "/etc/systemd/system/haproxy.service.d"
OVERRIDE_FILE = OVERRIDE_DIR + "/override.conf"


def test_systemd_override_directory_exists(host):
    """The systemd override directory should exist."""
    d = host.file(OVERRIDE_DIR)
    assert d.exists
    assert d.is_directory


def test_systemd_override_file_exists(host):
    """The override.conf should be deployed."""
    f = host.file(OVERRIDE_FILE)
    assert f.exists
    assert f.is_file


def test_systemd_override_permissions(host):
    f = host.file(OVERRIDE_FILE)
    assert f.user == "root"
    assert f.group == "root"
    assert oct(f.mode) == "0o644"


def test_systemd_override_has_managed_header(host):
    assert host.file(OVERRIDE_FILE).contains("Ansible managed")


def test_systemd_override_has_service_section(host):
    assert host.file(OVERRIDE_FILE).contains(r"\[Service\]")


def test_systemd_override_limit_nofile(host):
    """LimitNOFILE should be set to 65536."""
    assert host.file(OVERRIDE_FILE).contains("LimitNOFILE=65536")


def test_systemd_effective_limit_nofile(host):
    """The running HAProxy process should have the elevated NOFILE limit."""
    cmd = host.run(
        "cat /proc/$(pgrep -o haproxy)/limits"
        " | grep 'Max open files'"
    )
    assert cmd.rc == 0
    # The line looks like: Max open files  65536  65536  files
    assert "65536" in cmd.stdout
