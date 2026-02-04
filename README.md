# Ansible Role: HAProxy

![CI](https://github.com/aimd54/ansible-role-haproxy/actions/workflows/ci.yml/badge.svg)

This Ansible role installs and configures HAProxy on Debian-based systems. It
uses raw directive lists for every HAProxy section, making the configuration
fully future-proof: any current or future HAProxy parameter works without
modifying the role or template.

## Installation

### Ansible Galaxy

```bash
ansible-galaxy install aimd54.haproxy
```

### requirements.yml

```yaml
roles:
  - name: aimd54.haproxy
```

Then install with:

```bash
ansible-galaxy install -r requirements.yml
```

## Requirements

- Ansible version 2.14 or higher.
- Supported operating systems:
  - Debian (bullseye, bookworm)
  - Ubuntu (focal, jammy)

### Collections

This role requires the following Ansible collection:

- `ansible.posix`

Install it with:

```bash
ansible-galaxy collection install ansible.posix
```

## Role Variables

### User-configurable (`defaults/main.yml`)

| Variable                  | Description                                        | Default                       |
|---------------------------|----------------------------------------------------|-------------------------------|
| `haproxy_version`         | HAProxy version branch for official repo.          | `"3.2"`                       |
| `haproxy_manage_config`   | Whether the role manages haproxy.cfg.              | `true`                        |
| `haproxy_config_path`     | Path to the configuration file.                    | `/etc/haproxy/haproxy.cfg`    |
| `haproxy_config_template` | Jinja2 template to use (override for custom).      | `haproxy.cfg.j2`              |
| `haproxy_config_validate` | Validate config before applying.                   | `true`                        |
| `haproxy_service_name`    | Systemd service name.                              | `haproxy`                     |
| `haproxy_service_enabled` | Enable service at boot.                            | `true`                        |
| `haproxy_service_state`   | Desired service state.                             | `started`                     |
| `haproxy_global_options`  | List of raw `global` directives.                   | *(sensible defaults)*         |
| `haproxy_defaults_options`| List of raw `defaults` directives.                 | *(sensible defaults)*         |
| `haproxy_frontends`       | List of `{name, options}` frontend sections.       | `[]`                          |
| `haproxy_backends`        | List of `{name, options}` backend sections.        | `[]`                          |
| `haproxy_listen_sections` | List of `{name, options}` listen sections.         | `[]`                          |
| `haproxy_resolvers`       | List of `{name, options}` resolver sections.       | `[]`                          |
| `haproxy_peers`           | List of `{name, options}` peers sections.          | `[]`                          |
| `haproxy_mailers`         | List of `{name, options}` mailers sections.        | `[]`                          |
| `haproxy_extra_config`    | Raw text appended at the end of haproxy.cfg.       | `""`                          |

### Internal (`vars/main.yml`)

| Variable                     | Description                              |
|------------------------------|------------------------------------------|
| `haproxy_apt_prerequisites`  | Packages required before adding the PPA. |
| `haproxy_apt_gpg_key_url`    | GPG key URL for the HAProxy repository.  |
| `haproxy_apt_repository`     | APT repository line.                     |
| `haproxy_apt_packages`       | Packages to install via apt.             |

## Dependencies

This role does not have any role dependencies. See [Collections](#collections)
above for required collection dependencies.

## Example Playbook

```yaml
- hosts: loadbalancers
  become: true
  roles:
    - role: aimd54.haproxy
      vars:
        haproxy_frontends:
          - name: http-in
            options:
              - bind *:80
              - default_backend webservers
        haproxy_backends:
          - name: webservers
            options:
              - balance roundrobin
              - option httpchk GET /
              - server web1 192.168.1.10:8080 check
              - server web2 192.168.1.11:8080 check
```

## Testing with Molecule

This role includes a Molecule test setup to verify its functionality.

### Setup

```bash
# Install uv (if not already installed)
# https://docs.astral.sh/uv/getting-started/installation/

# Install dependencies
uv sync

# Install required Ansible collections
uv run ansible-galaxy collection install ansible.posix
```

### Running Tests

```bash
# Full test lifecycle
uv run molecule test

# Or run individual steps
uv run molecule create      # Create Docker test container
uv run molecule converge    # Apply the role
uv run molecule verify      # Run testinfra test suite
uv run molecule destroy     # Tear down
```

## License

This role is licensed under the MIT License. See the [LICENSE](LICENSE) file for
more information.
