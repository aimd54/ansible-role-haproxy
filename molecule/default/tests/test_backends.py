"""Tests for HAProxy backend health and load balancing behavior."""

from conftest import STATS_SOCKET


def test_backend_webservers_servers_up(host):
    """Backend webservers should have servers in UP status."""
    cmd = host.run(
        "echo 'show stat' | socat stdio unix-connect:%s", STATS_SOCKET
    )
    assert cmd.rc == 0
    for line in cmd.stdout.splitlines():
        if line.startswith("webservers,web"):
            fields = line.split(",")
            status = fields[17]
            assert status == "UP", f"Server {fields[1]} status is {status}"


def test_backend_api_server_up(host):
    """Backend api-servers should have server in UP status."""
    cmd = host.run(
        "echo 'show stat' | socat stdio unix-connect:%s", STATS_SOCKET
    )
    assert cmd.rc == 0
    for line in cmd.stdout.splitlines():
        if line.startswith("api-servers,api"):
            fields = line.split(",")
            status = fields[17]
            assert status == "UP", f"Server {fields[1]} status is {status}"


def test_load_balancing_roundrobin(host):
    """Multiple requests to port 80 should be distributed across web1/web2."""
    for _ in range(10):
        host.run("wget -q -O /dev/null http://127.0.0.1:80")
    cmd = host.run(
        "echo 'show stat' | socat stdio unix-connect:%s", STATS_SOCKET
    )
    assert cmd.rc == 0
    sessions = {}
    for line in cmd.stdout.splitlines():
        if line.startswith("webservers,web"):
            fields = line.split(",")
            svname = fields[1]
            sessions[svname] = int(fields[7])
    assert sessions.get("web1", 0) > 0, "web1 received no requests"
    assert sessions.get("web2", 0) > 0, "web2 received no requests"
