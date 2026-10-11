# Repository Guidance

## Purpose and boundaries
- This repo owns downstream SQL analysis, metrics, and communication of synthetic website insights.
- Event generation belongs in `synthetic-website-data`; warehouse transformations belong in `synthetic-website-dbt`.

## Development
- Keep reusable data access in `src/synthetic_website_analytics/data/`, saved queries in `sql/`, and exploratory work in `notebooks/`.
- Parameterize queries through the existing connector rather than embedding credentials or dataset-specific connection strings.

## Validation
- Run `uv sync --group dev`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`, and `uv run pytest`.
- Run configured pre-commit hooks for repository-wide hygiene.

## Architecture constraints
- Keep analysis reproducible from the documented data interfaces.
- Do not move source generation or dbt model ownership into this package.

## Safety
- Keep local connection settings and generated analytics artifacts out of committed code.

## Branching strategy

- This repository uses **release-branch integration**. Create Story branches from the verified active `release/vX.Y.Z` and target Story PRs there; `main` changes only after the release readiness gate.
- Follow the [canonical branching and delivery policy](https://github.com/SpencerRWood/codex-config/blob/main/docs/branching-policy.md), available through the installed codex-config source path. Verify the strategy, release association, fetched base and PR target before implementation and record them in Story evidence. Story completion does not authorize publication or deployment; retain existing review, CI, security and rollback requirements.
