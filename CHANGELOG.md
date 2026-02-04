# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-02-04

### Added

- Install HAProxy from official APT repository on Debian/Ubuntu
- Raw directive lists for all 18 HAProxy configuration sections (global, defaults, frontends, backends, listen, resolvers, peers, mailers, userlists, caches, http-errors, rings, log-forwards, fcgi-apps, crt-stores, programs)
- Config validation with `haproxy -c -f` before applying
- Config backup before overwriting
- SSL certificate deployment
- DH parameter generation
- Custom error page deployment
- rsyslog configuration for HAProxy logging
- Logrotate configuration
- Kernel tuning via sysctl (somaxconn, ip_nonlocal_bind, tcp_tw_reuse)
- Systemd service overrides (LimitNOFILE)
- Optional management tool installation (socat, hatop)
- Molecule test suite with 16 testinfra modules
- GitHub Actions CI with yamllint, ansible-lint, and Molecule
- GitHub Actions release workflow for Ansible Galaxy publishing
