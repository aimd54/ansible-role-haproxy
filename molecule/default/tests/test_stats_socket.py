"""Tests for HAProxy stats socket — existence, info, stat output, maxconn."""

from conftest import STATS_SOCKET


def test_stats_socket_exists(host):
    """The admin stats socket should exist."""
    sock = host.file(STATS_SOCKET)
    assert sock.exists
    assert sock.is_socket


def test_stats_socket_show_info(host):
    """Stats socket should respond to 'show info' command."""
    cmd = host.run(
        "echo 'show info' | socat stdio unix-connect:%s", STATS_SOCKET
    )
    assert cmd.rc == 0
    assert "Name: HAProxy" in cmd.stdout


def test_stats_socket_show_stat(host):
    """Stats socket should respond to 'show stat' and list frontends/backends."""
    cmd = host.run(
        "echo 'show stat' | socat stdio unix-connect:%s", STATS_SOCKET
    )
    assert cmd.rc == 0
    assert "http-in" in cmd.stdout
    assert "https-in" in cmd.stdout
    assert "webservers" in cmd.stdout
    assert "api-servers" in cmd.stdout


def test_stats_socket_maxconn(host):
    """Stats socket show info should report the configured maxconn."""
    cmd = host.run(
        "echo 'show info' | socat stdio unix-connect:%s", STATS_SOCKET
    )
    assert cmd.rc == 0
    assert "Maxconn: 4096" in cmd.stdout
