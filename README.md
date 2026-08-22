# template-python-library

A minimal, typed Python library template with `uv`, Ruff, mypy, pytest,
pre-commit, coverage, GitHub Actions, and semantic-release already wired
together.

## Use This Template

When creating a fresh project from this baseline, make these changes before
writing application code:

1. Rename the package directory:

   ```sh
   mv src/package_name src/your_package_name
   ```

2. Update package references in `pyproject.toml`:

   ```toml
   [project]
   name = "your-project-name"
   description = "..."

   [tool.hatch.build.targets.wheel]
   packages = ["src/your_package_name"]

   [tool.coverage.run]
   source = ["your_package_name"]
   ```

3. Update imports and tests that still mention `package_name`.

4. Update metadata in `pyproject.toml`:

   - `authors`
   - `classifiers`
   - `requires-python`, if the project should not require Python 3.14
   - runtime `dependencies`
   - `LICENSE`, if MIT is not appropriate

5. Update workflow commands if the package name changed:

   ```yaml
   uv run pytest --cov=your_package_name --cov-report=term-missing
   ```

6. Refresh the lockfile after dependency or Python-version changes:

   ```sh
   uv lock
   uv sync --frozen --group dev
   ```

7. Replace this README content with project-specific docs after the project is
   initialized.

## Project Layout

```text
src/package_name/
  __init__.py
  py.typed
tests/
  unit/
    test_placeholder.py
```

This template uses the `src/` layout. Keep importable library code under
`src/<package_name>/` and tests under `tests/`. The `py.typed` marker declares
the package as typed for downstream users.

## Local Setup

Install dependencies into the local environment:

```sh
uv sync --frozen --group dev
```

Install pre-commit hooks:

```sh
uv run pre-commit install
```

Run all checks locally:

```sh
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov=package_name --cov-report=term-missing
uv run pre-commit run --all-files
```

Use Ruff to apply safe fixes:

```sh
uv run ruff check --fix .
uv run ruff format .
```

## Ruff And Lint Rules

Ruff is configured in `pyproject.toml` with:

- line length: `88`
- source roots: `src`, `tests`
- formatter: double quotes, spaces, native line endings
- selected rules: Pyflakes, pycodestyle, import sorting, bugbear,
  comprehensions, datetime, pathlib, pytest style, Ruff-specific rules, and
  several cleanup/simplification families

The template intentionally treats linting as part of the normal development
loop. Run `uv run ruff check .` before pushing, and use
`uv run ruff check --fix .` for mechanical fixes.

Tests ignore `S101` so normal `assert` statements are allowed.

## Type Checking

mypy runs in strict mode over `src` and `tests`:

```sh
uv run mypy
```

If the package is renamed, keep `mypy_path = "src"` and update imports rather
than adding path hacks.

## Tests And Coverage

pytest is configured with strict config and marker validation:

```sh
uv run pytest
```

CI runs coverage and requires at least 90 percent:

```sh
uv run pytest --cov=package_name --cov-report=term-missing
```

When the package is renamed, update both `[tool.coverage.run].source` and the
workflow `--cov=` arguments.

## Pre-commit

Pre-commit runs:

- `no-commit-to-branch` for `main`
- large-file checks
- merge-conflict checks
- TOML and YAML validation
- end-of-file fixing
- trailing-whitespace cleanup
- Ruff lint with `--fix`
- Ruff format

Normal local work should happen on a branch. If you intentionally need to
commit directly to `main` during repository bootstrap, use:

```sh
SKIP=no-commit-to-branch git commit -m "..."
```

The GitHub workflows also set `SKIP=no-commit-to-branch` when running
pre-commit, because automation runs against `main` during releases.

## GitHub Actions

There are two workflows:

- `CI`: runs on pull requests targeting `main` and pushes to non-`main`
  branches.
- `Release`: runs on pushes to `main`.

Both workflows:

1. Check out the repository.
2. Set up Python 3.14.
3. Install `uv` with `astral-sh/setup-uv@v9.0.0`.
4. Run `uv sync --frozen --group dev`.
5. Run Ruff lint.
6. Run Ruff format check.
7. Run mypy.
8. Run pytest with coverage.
9. Run pre-commit.

The release workflow then runs:

```sh
uv run semantic-release version --vcs-release
```

Because workflows use `uv sync --frozen`, any dependency change must include an
updated `uv.lock`.

## Semantic Release

semantic-release is configured to:

- parse conventional commits
- update `project.version` in `pyproject.toml`
- create tags like `v0.1.1`
- create GitHub releases
- publish release assets to the VCS release

Version bumps come from commit messages:

- `fix:` and `perf:` create patch releases
- `feat:` creates minor releases
- breaking changes create major releases
- `chore:`, `ci:`, `docs:`, `refactor:`, `style:`, and `test:` do not create
  releases by themselves

For `0.x` versions, `major_on_zero = true` is enabled, so breaking changes are
handled deliberately even before `1.0.0`.

The workflow uses `GITHUB_TOKEN` from GitHub Actions; no extra token is needed
for normal repository releases.

## Bootstrap Checklist

Before the first project-specific commit:

- Rename `package_name`.
- Update package metadata in `pyproject.toml`.
- Update coverage and workflow package names.
- Run `uv lock` after dependency changes.
- Run `uv sync --frozen --group dev`.
- Run Ruff, mypy, pytest with coverage, and pre-commit.
- Push once and confirm GitHub Actions passes.
