"""Tests for HAProxy custom error pages deployment."""


def test_custom_error_page_exists(host):
    """The custom maintenance error page should be deployed."""
    f = host.file("/etc/haproxy/errors/maintenance.http")
    assert f.exists
    assert f.is_file


def test_custom_error_page_content(host):
    """The custom error page should contain the expected content."""
    f = host.file("/etc/haproxy/errors/maintenance.http")
    assert f.contains("503 Service Unavailable")
    assert f.contains("Under Maintenance")


def test_custom_error_page_permissions(host):
    f = host.file("/etc/haproxy/errors/maintenance.http")
    assert f.user == "root"
    assert f.group == "root"
    assert oct(f.mode) == "0o644"


def test_errors_directory_exists(host):
    """The errors directory should exist."""
    d = host.file("/etc/haproxy/errors")
    assert d.exists
    assert d.is_directory


def test_standard_error_files_still_present(host):
    """Standard error files should not be removed by custom pages."""
    for code in ["400", "403", "408", "500", "502", "503", "504"]:
        f = host.file(f"/etc/haproxy/errors/{code}.http")
        assert f.exists, f"Error file {code}.http missing"
        assert f.size > 0, f"Error file {code}.http is empty"
