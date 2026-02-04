# Contributing

Contributions are welcome. Please follow these guidelines.

## Reporting Issues

Open a GitHub issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- OS and Ansible version

## Pull Requests

1. Fork the repository and create a feature branch
2. Make your changes
3. Ensure linters and tests pass (see below)
4. Submit a PR against `main`

## Development Setup

```bash
# Install uv (if not already installed)
# https://docs.astral.sh/uv/getting-started/installation/

# Install dependencies
uv sync

# Install required Ansible collections
uv run ansible-galaxy collection install ansible.posix

# Run linters
uv run yamllint .
uv run ansible-lint

# Run full Molecule test suite (requires Docker)
uv run molecule test
```

## Code Style

- Use fully qualified collection names (FQCN) for all modules (e.g., `ansible.builtin.apt`, `ansible.posix.sysctl`)
- Follow the raw directive list pattern for HAProxy configuration sections
- Keep YAML files valid against the project's `.yamllint` and `.ansible-lint` configs
