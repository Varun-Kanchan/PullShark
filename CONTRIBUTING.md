# Contributing to PullShark

Thanks for your interest in contributing! 🦈

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/PullShark.git
   cd PullShark
   ```
3. **Install** in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Branch Naming

- `feature/your-feature` — new features
- `fix/your-bugfix` — bug fixes
- `docs/your-docs` — documentation changes

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=pullshark --cov-report=term-missing
```

### Linting

```bash
ruff check pullshark/ tests/
```

### Before Submitting

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Code is linted (`ruff check pullshark/ tests/`)
- [ ] New features have tests
- [ ] CHANGELOG.md is updated (add entry at the top)
- [ ] README.md is updated if API changes

## Pull Request Guidelines

1. **One feature per PR** — keep changes focused
2. **Write clear commit messages** — explain *what* and *why*
3. **Update CHANGELOG.md** — add a new entry under `[Unreleased]` at the top
4. **Add tests** — new code should have test coverage
5. **Keep it backwards compatible** — don't break existing CLI args or config fields

## Reporting Issues

- Use [GitHub Issues](https://github.com/Shineii86/PullShark/issues)
- Include steps to reproduce
- Include your Python version (`python --version`)
- Include PullShark version (`python -c "import pullshark; print(pullshark.__version__)"`)

## Code Style

- Python 3.8+ compatible
- Type hints on all public functions
- Docstrings on all public methods
- Keep functions small and focused

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
