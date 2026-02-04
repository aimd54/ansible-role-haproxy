"""Tests for HAProxy networking — listening sockets and HTTP responses."""


def test_listening_port_80(host):
    """HAProxy should be listening on port 80 (HTTP frontend)."""
    assert host.socket("tcp://0.0.0.0:80").is_listening


def test_listening_port_443(host):
    """HAProxy should be listening on port 443 (HTTPS frontend)."""
    assert host.socket("tcp://0.0.0.0:443").is_listening


def test_listening_port_8404(host):
    """HAProxy should be listening on port 8404 (stats)."""
    assert host.socket("tcp://0.0.0.0:8404").is_listening


def test_http_response_port_80(host):
    """HTTP request through port 80 should reach the backend."""
    cmd = host.run("wget -q -O /dev/null http://127.0.0.1:80")
    assert cmd.rc == 0


def test_https_response_port_443(host):
    """HTTPS request through port 443 should reach the backend."""
    cmd = host.run(
        "wget -q --no-check-certificate -O /dev/null https://127.0.0.1:443"
    )
    assert cmd.rc == 0


def test_stats_page(host):
    """Stats page should be accessible on port 8404."""
    cmd = host.run("wget -q -O /dev/null http://127.0.0.1:8404/stats")
    assert cmd.rc == 0
