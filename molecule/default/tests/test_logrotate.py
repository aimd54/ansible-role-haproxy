"""Tests for HAProxy logrotate configuration."""


def test_logrotate_config_exists(host):
    """The logrotate config for HAProxy should be deployed."""
    cfg = host.file("/etc/logrotate.d/haproxy")
    assert cfg.exists
    assert cfg.is_file


def test_logrotate_config_permissions(host):
    cfg = host.file("/etc/logrotate.d/haproxy")
    assert cfg.user == "root"
    assert cfg.group == "root"
    assert oct(cfg.mode) == "0o644"


def test_logrotate_config_has_managed_header(host):
    assert host.file("/etc/logrotate.d/haproxy").contains("Ansible managed")


def test_logrotate_config_references_log_file(host):
    assert host.file("/etc/logrotate.d/haproxy").contains("/var/log/haproxy.log")


def test_logrotate_config_frequency(host):
    assert host.file("/etc/logrotate.d/haproxy").contains("daily")


def test_logrotate_config_rotate_count(host):
    assert host.file("/etc/logrotate.d/haproxy").contains("rotate 14")


def test_logrotate_config_compress(host):
    cfg = host.file("/etc/logrotate.d/haproxy")
    assert cfg.contains("compress")
    assert cfg.contains("delaycompress")


def test_logrotate_config_options(host):
    cfg = host.file("/etc/logrotate.d/haproxy")
    assert cfg.contains("missingok")
    assert cfg.contains("notifempty")
    assert cfg.contains("sharedscripts")


def test_logrotate_config_postrotate(host):
    assert host.file("/etc/logrotate.d/haproxy").contains("postrotate")
