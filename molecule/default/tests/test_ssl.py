"""Tests for HAProxy SSL/TLS — protocol enforcement."""


def test_tls_version_minimum(host):
    """HAProxy should reject TLS versions below 1.2."""
    cmd = host.run(
        "openssl s_client -connect 127.0.0.1:443 -tls1_1 < /dev/null 2>&1"
    )
    assert cmd.rc != 0 or "alert protocol version" in cmd.stderr + cmd.stdout


def test_tls_1_2_accepted(host):
    """HAProxy should accept TLS 1.2 connections."""
    cmd = host.run(
        "openssl s_client -connect 127.0.0.1:443 -tls1_2 < /dev/null 2>&1"
    )
    combined = cmd.stdout + cmd.stderr
    assert "CONNECTED" in combined


def test_tls_certificate_cn(host):
    """The TLS certificate CN should be localhost."""
    cmd = host.run(
        "echo | openssl s_client -connect 127.0.0.1:443 2>/dev/null"
        " | openssl x509 -noout -subject"
    )
    assert cmd.rc == 0
    assert "CN" in cmd.stdout
    assert "localhost" in cmd.stdout
