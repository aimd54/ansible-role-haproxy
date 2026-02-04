"""Tests for HAProxy kernel tuning (sysctl)."""


def test_sysctl_somaxconn(host):
    """net.core.somaxconn should be set to 4096."""
    cmd = host.run("sysctl -n net.core.somaxconn")
    assert cmd.rc == 0
    assert cmd.stdout.strip() == "4096"


def test_sysctl_ip_nonlocal_bind(host):
    """net.ipv4.ip_nonlocal_bind should be set to 1."""
    cmd = host.run("sysctl -n net.ipv4.ip_nonlocal_bind")
    assert cmd.rc == 0
    assert cmd.stdout.strip() == "1"


def test_sysctl_conf_file_exists(host):
    """A sysctl config file should be present for persistence."""
    # ansible.posix.sysctl writes to /etc/sysctl.d/ or /etc/sysctl.conf
    cmd = host.run("sysctl -a 2>/dev/null | grep net.core.somaxconn")
    assert cmd.rc == 0
    assert "4096" in cmd.stdout
