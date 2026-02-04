"""Tests for HAProxy rsyslog integration."""


def test_rsyslog_config_exists(host):
    """The rsyslog config for HAProxy should be deployed."""
    cfg = host.file("/etc/rsyslog.d/49-haproxy.conf")
    assert cfg.exists
    assert cfg.is_file


def test_rsyslog_config_permissions(host):
    cfg = host.file("/etc/rsyslog.d/49-haproxy.conf")
    assert cfg.user == "root"
    assert cfg.group == "root"
    assert oct(cfg.mode) == "0o644"


def test_rsyslog_config_has_managed_header(host):
    assert host.file("/etc/rsyslog.d/49-haproxy.conf").contains("Ansible managed")


def test_rsyslog_config_references_log_file(host):
    """Config should direct HAProxy logs to /var/log/haproxy.log."""
    assert host.file("/etc/rsyslog.d/49-haproxy.conf").contains(
        "/var/log/haproxy.log"
    )


def test_rsyslog_config_references_haproxy(host):
    """Config should filter on haproxy program name."""
    assert host.file("/etc/rsyslog.d/49-haproxy.conf").contains("haproxy")


def test_rsyslog_chroot_dev_directory(host):
    """The chroot /var/lib/haproxy/dev directory should exist for syslog."""
    d = host.file("/var/lib/haproxy/dev")
    assert d.exists
    assert d.is_directory


def test_rsyslog_service_running(host):
    """rsyslog should be running after config deployment."""
    assert host.service("rsyslog").is_running
