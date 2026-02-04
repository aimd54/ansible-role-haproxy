"""Tests for HAProxy configuration file — existence, permissions, syntax,
section content, and section ordering.

Covers: haproxy_manage_config, haproxy_config_path, haproxy_config_template,
haproxy_config_validate, haproxy_global_options, haproxy_defaults_options,
haproxy_frontends, haproxy_backends, haproxy_listen_sections,
haproxy_userlists, haproxy_caches, haproxy_http_errors, haproxy_rings,
haproxy_log_forwards, haproxy_resolvers, haproxy_peers, haproxy_mailers,
haproxy_extra_config.
"""

from conftest import CFG


# ---------------------------------------------------------------------------
# File existence, permissions, header
# ---------------------------------------------------------------------------

def test_config_file_exists(host):
    """haproxy.cfg should exist at the default path."""
    cfg = host.file(CFG)
    assert cfg.exists
    assert cfg.is_file


def test_config_file_permissions(host):
    """haproxy.cfg should be owned by root with 0644 permissions."""
    cfg = host.file(CFG)
    assert cfg.user == "root"
    assert cfg.group == "root"
    assert oct(cfg.mode) == "0o644"


def test_config_has_ansible_managed_header(host):
    """Config should contain the Ansible managed header."""
    assert host.file(CFG).contains("Ansible managed")


def test_config_syntax_valid(host):
    """haproxy -c should validate the configuration successfully."""
    cmd = host.run("haproxy -c -f %s", CFG)
    assert cmd.rc == 0


# ---------------------------------------------------------------------------
# Global section (haproxy_global_options)
# ---------------------------------------------------------------------------

def test_global_section_exists(host):
    assert host.file(CFG).contains("^global")


def test_global_log(host):
    cfg = host.file(CFG)
    assert cfg.contains("log /dev/log local0")
    assert cfg.contains("log /dev/log local1 notice")


def test_global_chroot(host):
    assert host.file(CFG).contains("chroot /var/lib/haproxy")


def test_global_stats_socket(host):
    assert host.file(CFG).contains("stats socket /run/haproxy/admin.sock")


def test_global_user_group(host):
    cfg = host.file(CFG)
    assert cfg.contains("user haproxy")
    assert cfg.contains("group haproxy")


def test_global_daemon(host):
    assert host.file(CFG).contains("daemon")


def test_global_maxconn(host):
    assert host.file(CFG).contains("maxconn 4096")


def test_global_ssl_bind_ciphers(host):
    assert host.file(CFG).contains("ssl-default-bind-ciphers")


def test_global_ssl_bind_options(host):
    assert host.file(CFG).contains("ssl-default-bind-options ssl-min-ver TLSv1.2")


# ---------------------------------------------------------------------------
# Defaults section (haproxy_defaults_options)
# ---------------------------------------------------------------------------

def test_defaults_section_exists(host):
    assert host.file(CFG).contains("^defaults")


def test_defaults_log(host):
    assert host.file(CFG).contains("log global")


def test_defaults_mode(host):
    assert host.file(CFG).contains("mode http")


def test_defaults_option_httplog(host):
    assert host.file(CFG).contains("option httplog")


def test_defaults_option_dontlognull(host):
    assert host.file(CFG).contains("option dontlognull")


def test_defaults_option_forwardfor(host):
    assert host.file(CFG).contains("option forwardfor")


def test_defaults_option_http_server_close(host):
    assert host.file(CFG).contains("option http-server-close")


def test_defaults_timeout_connect(host):
    assert host.file(CFG).contains("timeout connect 5000ms")


def test_defaults_timeout_client(host):
    assert host.file(CFG).contains("timeout client 50000ms")


def test_defaults_timeout_server(host):
    assert host.file(CFG).contains("timeout server 50000ms")


def test_defaults_errorfiles(host):
    cfg = host.file(CFG)
    for code in ["400", "403", "408", "500", "502", "503", "504"]:
        assert cfg.contains(f"errorfile {code}")


# ---------------------------------------------------------------------------
# Frontend sections (haproxy_frontends)
# ---------------------------------------------------------------------------

def test_frontend_http_exists(host):
    assert host.file(CFG).contains("^frontend http-in")


def test_frontend_http_bind(host):
    assert host.file(CFG).contains(r"bind \*:80")


def test_frontend_http_default_backend(host):
    assert host.file(CFG).contains("default_backend webservers")


def test_frontend_https_exists(host):
    assert host.file(CFG).contains("^frontend https-in")


def test_frontend_https_ssl_bind(host):
    assert host.file(CFG).contains(
        r"bind \*:443 ssl crt /etc/haproxy/ssl/test.pem"
    )


def test_frontend_https_forwarded_proto(host):
    assert host.file(CFG).contains(
        "http-request set-header X-Forwarded-Proto https"
    )


# ---------------------------------------------------------------------------
# Backend sections (haproxy_backends)
# ---------------------------------------------------------------------------

def test_backend_webservers_exists(host):
    assert host.file(CFG).contains("^backend webservers")


def test_backend_webservers_balance(host):
    assert host.file(CFG).contains("balance roundrobin")


def test_backend_webservers_healthcheck(host):
    assert host.file(CFG).contains("option httpchk GET /")


def test_backend_webservers_server_web1(host):
    assert host.file(CFG).contains("server web1 127.0.0.1:8080 check")


def test_backend_webservers_server_web2(host):
    assert host.file(CFG).contains("server web2 127.0.0.1:8081 check")


def test_backend_api_exists(host):
    assert host.file(CFG).contains("^backend api-servers")


def test_backend_api_balance(host):
    assert host.file(CFG).contains("balance leastconn")


def test_backend_api_server(host):
    assert host.file(CFG).contains("server api1 127.0.0.1:8080 check")


# ---------------------------------------------------------------------------
# Listen sections (haproxy_listen_sections)
# ---------------------------------------------------------------------------

def test_listen_stats_exists(host):
    assert host.file(CFG).contains("^listen stats")


def test_listen_stats_bind(host):
    assert host.file(CFG).contains(r"bind \*:8404")


def test_listen_stats_enable(host):
    assert host.file(CFG).contains("stats enable")


def test_listen_stats_uri(host):
    assert host.file(CFG).contains("stats uri /stats")


def test_listen_stats_refresh(host):
    assert host.file(CFG).contains("stats refresh 10s")


# ---------------------------------------------------------------------------
# Userlist sections (haproxy_userlists)
# ---------------------------------------------------------------------------

def test_userlist_section_exists(host):
    assert host.file(CFG).contains("^userlist myusers")


def test_userlist_group(host):
    assert host.file(CFG).contains("group admins users admin")


def test_userlist_user_admin(host):
    assert host.file(CFG).contains("user admin insecure-password adminpass")


def test_userlist_user_viewer(host):
    assert host.file(CFG).contains("user viewer insecure-password viewerpass")


# ---------------------------------------------------------------------------
# Cache sections (haproxy_caches)
# ---------------------------------------------------------------------------

def test_cache_section_exists(host):
    assert host.file(CFG).contains("^cache mycache")


def test_cache_total_max_size(host):
    assert host.file(CFG).contains("total-max-size 64")


def test_cache_max_object_size(host):
    assert host.file(CFG).contains("max-object-size 10000")


def test_cache_max_age(host):
    assert host.file(CFG).contains("max-age 30")


# ---------------------------------------------------------------------------
# HTTP-errors sections (haproxy_http_errors)
# ---------------------------------------------------------------------------

def test_http_errors_section_exists(host):
    assert host.file(CFG).contains("^http-errors custom-errors")


def test_http_errors_errorfile(host):
    assert host.file(CFG).contains("errorfile 503 /etc/haproxy/errors/503.http")


# ---------------------------------------------------------------------------
# Ring sections (haproxy_rings)
# ---------------------------------------------------------------------------

def test_ring_section_exists(host):
    assert host.file(CFG).contains("^ring myring")


def test_ring_description(host):
    assert host.file(CFG).contains("description")


def test_ring_format(host):
    assert host.file(CFG).contains("format rfc5424")


def test_ring_maxlen(host):
    assert host.file(CFG).contains("maxlen 1200")


def test_ring_size(host):
    assert host.file(CFG).contains("size 32764")


# ---------------------------------------------------------------------------
# Log-forward sections (haproxy_log_forwards)
# ---------------------------------------------------------------------------

def test_log_forward_section_exists(host):
    assert host.file(CFG).contains("^log-forward mylogforward")


def test_log_forward_dgram_bind(host):
    assert host.file(CFG).contains(r"dgram-bind \*:1514")


def test_log_forward_log_ring(host):
    assert host.file(CFG).contains("log ring@myring local0")


# ---------------------------------------------------------------------------
# Resolvers sections (haproxy_resolvers)
# ---------------------------------------------------------------------------

def test_resolvers_section_exists(host):
    assert host.file(CFG).contains("^resolvers mydns")


def test_resolvers_nameserver(host):
    assert host.file(CFG).contains("nameserver dns1 127.0.0.1:53")


def test_resolvers_retries(host):
    assert host.file(CFG).contains("resolve_retries 3")


def test_resolvers_timeout_resolve(host):
    assert host.file(CFG).contains("timeout resolve 1s")


def test_resolvers_timeout_retry(host):
    assert host.file(CFG).contains("timeout retry 1s")


def test_resolvers_hold_valid(host):
    assert host.file(CFG).contains("hold valid 10s")


# ---------------------------------------------------------------------------
# Peers sections (haproxy_peers)
# ---------------------------------------------------------------------------

def test_peers_section_exists(host):
    assert host.file(CFG).contains("^peers mypeers")


def test_peers_entry(host):
    assert host.file(CFG).contains("peer haproxy1 127.0.0.1:10000")


# ---------------------------------------------------------------------------
# Mailers sections (haproxy_mailers)
# ---------------------------------------------------------------------------

def test_mailers_section_exists(host):
    assert host.file(CFG).contains("^mailers mymailers")


def test_mailers_entry(host):
    assert host.file(CFG).contains("mailer smtp1 127.0.0.1:25")


# ---------------------------------------------------------------------------
# Extra config (haproxy_extra_config)
# ---------------------------------------------------------------------------

def test_extra_config_line1(host):
    assert host.file(CFG).contains("Custom extra configuration")


def test_extra_config_line2(host):
    assert host.file(CFG).contains("This tests the haproxy_extra_config variable")


# ---------------------------------------------------------------------------
# Section ordering in rendered config
# ---------------------------------------------------------------------------

def test_config_section_ordering(host):
    """All sections should appear in the correct template order."""
    content = host.run("cat %s", CFG).stdout
    sections = [
        "global",
        "defaults",
        "userlist",
        "cache",
        "ring",
        "crt-store",
        "fcgi-app",
        "program",
        "http-errors",
        "frontend",
        "backend",
        "listen",
        "log-forward",
        "resolvers",
        "peers",
        "mailers",
    ]
    positions = []
    for section in sections:
        pos = content.find(f"\n{section}")
        if pos == -1:
            pos = content.find(section)
        if pos == -1:
            continue
        positions.append((section, pos))
    for i in range(1, len(positions)):
        prev_name, prev_pos = positions[i - 1]
        curr_name, curr_pos = positions[i]
        assert prev_pos < curr_pos, (
            f"{prev_name} (pos {prev_pos}) should come before "
            f"{curr_name} (pos {curr_pos})"
        )
