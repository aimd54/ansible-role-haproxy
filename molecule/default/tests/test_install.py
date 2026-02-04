"""Tests for HAProxy package installation and APT infrastructure."""


def test_haproxy_is_installed(host):
    """HAProxy package should be installed."""
    assert host.package("haproxy").is_installed


def test_haproxy_binary_exists(host):
    """HAProxy binary should be present in PATH."""
    assert host.exists("haproxy")


def test_haproxy_version(host):
    """HAProxy binary should report a version string."""
    cmd = host.run("haproxy -v")
    assert cmd.rc == 0
    assert "HAProxy version" in cmd.stdout


def test_apt_keyring_file_exists(host):
    """The HAProxy APT keyring file should be present."""
    keyring = host.file("/etc/apt/keyrings/haproxy-archive-keyring.gpg")
    assert keyring.exists
    assert keyring.is_file
    assert keyring.size > 0


def test_apt_sources_list_exists(host):
    """The HAProxy sources.list entry should exist."""
    sources = host.file("/etc/apt/sources.list.d/haproxy.list")
    assert sources.exists
    assert sources.is_file


def test_apt_sources_list_content(host):
    """The sources.list should reference haproxy.debian.net with signed-by."""
    sources = host.file("/etc/apt/sources.list.d/haproxy.list")
    assert sources.contains("haproxy.debian.net")
    assert sources.contains("signed-by")
    assert sources.contains("backports")
