"""Tests for HAProxy SSL certificate deployment and DH parameters."""


def test_ssl_directory_exists(host):
    """The SSL directory should exist with restricted permissions."""
    d = host.file("/etc/haproxy/ssl")
    assert d.exists
    assert d.is_directory
    assert oct(d.mode) == "0o750"


def test_ssl_cert_exists(host):
    """SSL certificate file should exist (deployed by prepare)."""
    cert = host.file("/etc/haproxy/ssl/test.pem")
    assert cert.exists
    assert cert.is_file


def test_dhparam_file_exists(host):
    """DH parameters file should have been generated."""
    dhp = host.file("/etc/haproxy/ssl/dhparam.pem")
    assert dhp.exists
    assert dhp.is_file


def test_dhparam_file_permissions(host):
    dhp = host.file("/etc/haproxy/ssl/dhparam.pem")
    assert dhp.user == "root"
    assert dhp.group == "root"
    assert oct(dhp.mode) == "0o640"


def test_dhparam_file_is_valid(host):
    """The DH parameters file should be valid PEM."""
    cmd = host.run("openssl dhparam -in /etc/haproxy/ssl/dhparam.pem -check -noout")
    assert cmd.rc == 0
