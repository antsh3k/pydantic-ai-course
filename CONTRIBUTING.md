# Contributing

Thanks for your interest in improving this course! We welcome contributions that
improve the materials and keep them up-to-date with the latest Pydantic ecosystem
developments.

By participating in this project, you agree to abide by our
[Code of Conduct](CODE_OF_CONDUCT.md).

## Scope

This course focuses exclusively on the **Pydantic ecosystem** (PydanticAI, Pydantic,
pydantic-evals, Logfire). Contributions involving other frameworks or libraries
should be discussed first via an issue.

## Types of contributions welcome

- Bug fixes in existing notebooks
- Updates for new PydanticAI releases
- Additional exercises or examples
- Improved explanations and documentation
- Typo corrections

## Development setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies, including the dev group
uv sync --group dev

# Install pre-commit hooks (runs nbstripout to clear notebook outputs)
pre-commit install
```

Notebook outputs are stripped automatically on commit via `nbstripout`, which keeps
diffs clean and avoids committing execution results or secrets.

## Making a change

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and run the affected notebooks end-to-end to confirm they work.
3. Ensure pre-commit passes: `pre-commit run --all-files`
4. Open a pull request with a clear description of what changed and why.

## Reporting issues

Found a bug or have a suggestion? Please open an issue using one of the templates
in `.github/ISSUE_TEMPLATE/`.
