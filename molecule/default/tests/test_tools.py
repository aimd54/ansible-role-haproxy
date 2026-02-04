"""Tests for HAProxy management tools installation."""


def test_socat_is_installed(host):
    """socat should be installed for stats socket management."""
    assert host.package("socat").is_installed


def test_socat_binary_exists(host):
    assert host.exists("socat")


def test_hatop_is_installed(host):
    """hatop should be installed for HAProxy monitoring."""
    assert host.package("hatop").is_installed
