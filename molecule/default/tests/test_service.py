"""Tests for HAProxy service state, process model, and logging."""


def test_haproxy_service_running(host):
    """HAProxy service should be running (haproxy_service_state=started)."""
    assert host.service("haproxy").is_running


def test_haproxy_service_enabled(host):
    """HAProxy service should be enabled at boot (haproxy_service_enabled=true)."""
    assert host.service("haproxy").is_enabled


def test_haproxy_master_process_exists(host):
    """HAProxy master process should be running."""
    cmd = host.run("pgrep -c haproxy")
    assert cmd.rc == 0
    # master + at least one worker
    assert int(cmd.stdout.strip()) >= 2


def test_haproxy_worker_runs_as_haproxy_user(host):
    """HAProxy worker processes should run as the haproxy user."""
    cmd = host.run("ps -C haproxy -o user= | sort -u")
    assert cmd.rc == 0
    users = cmd.stdout.strip().split("\n")
    # worker runs as haproxy; master may run as root
    assert "haproxy" in users


def test_haproxy_chroot_directory_exists(host):
    """The chroot directory /var/lib/haproxy should exist."""
    d = host.file("/var/lib/haproxy")
    assert d.exists
    assert d.is_directory


def test_haproxy_journal_logs(host):
    """HAProxy should have log entries in the systemd journal."""
    cmd = host.run("journalctl -u haproxy --no-pager -n 20")
    assert cmd.rc == 0
    assert "haproxy" in cmd.stdout.lower()
