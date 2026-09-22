# Development

## Setup

```bash
git clone https://github.com/nghialuffy/tcbs-api
cd tcbs-api
uv sync
```

`uv sync` installs the `dev` dependency group — ruff, mypy and pytest — plus the MkDocs stack
this site is built with, all against the project's own interpreter. With pip, the equivalent is
`pip install -e ".[dev,docs]"`.

## Checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy tcbs_api
uv run pytest
uv build
```

## Building this documentation

```bash
uv run mkdocs serve        # http://127.0.0.1:8000, reloads on change
uv run mkdocs build --strict
```

`strict: true` in `mkdocs.yml` turns MkDocs warnings — a broken internal link, an unresolvable
anchor — into build failures, so the check above is the one to run before pushing. The `watch`
list makes `mkdocs serve` reload when the library changes too, not only when the Markdown does.

The API reference is generated: the pages under `docs/api/` are a list of `:::` directives naming
modules, and [mkdocstrings](https://mkdocstrings.github.io/) renders the module docstring,
signatures and model fields out of the installed package. Those pages need editing only when a
module is added — but every field description and docstring you write shows up on them, which is
why they are worth writing well.

Two pages include text rather than repeating it: `docs/limitations.md` pulls the drift table out of
`README.md` with `--8<-- "README.md:drift-table"`, and `docs/changelog.md` pulls in `CHANGELOG.md`.
Edit those in the source file, not on the docs page.

## Checking the DTOs against the live API

The models follow real payloads where TCBS's OpenAPI document is wrong (see
[Known limitations](limitations.md#the-models-follow-live-responses-where-the-document-is-wrong)),
and `tests/integration_test.py` is what keeps that honest. Paste a JWT into `ACCESS_TOKEN` at the
top of that file, then either of:

```bash
uv run pytest tests/integration_test.py      # skips while the token is empty
uv run python tests/integration_test.py
```

It calls every wrapped endpoint once and reports, per endpoint, anything it could not decode, any
key no model declares, and the declared fields the payload left out. A field TCBS stopped
sending, or a new one it started sending, shows up there first.

## Publishing this documentation

The site is hosted on [Read the Docs](https://readthedocs.org/) at
<https://tcbs-api.readthedocs.io/>. `.readthedocs.yaml` in the repository is the whole
configuration: it pins the build image and Python, points at `mkdocs.yml`, and installs the
`docs` extra that `pyproject.toml` defines.

One-time setup in the Read the Docs web UI: **Add project → Import a Repository**, pick
`nghialuffy/tcbs-api`, and leave the defaults. The project slug has to be `tcbs-api` for the site
to land on the URL above; a different slug means a different `readthedocs.io` subdomain, in which
case update `site_url` in `mkdocs.yml` to match.

After that, every push to the default branch builds a new version, and every pull request builds
a preview, with no CI configuration and no tokens in the repository — the build runs on Read the
Docs' side.

## Releasing

Releases are automated by
[`.github/workflows/publish.yml`](https://github.com/nghialuffy/tcbs-api/blob/main/.github/workflows/publish.yml)
using PyPI trusted publishing (OIDC), so no API token is stored in the repository.
`tcbs_api/__init__.py` is the single source of truth for the version — `pyproject.toml` reads it
dynamically, so there is nothing to keep in sync. Step by step:

1. Bump `__version__` in `tcbs_api/__init__.py` and add a matching [Changelog](changelog.md)
   entry.
2. Commit, then tag and push:
   ```bash
   git commit -am "release: vX.Y.Z"
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin main --follow-tags
   ```
3. Publish a GitHub Release for that tag. The workflow builds the sdist and wheel, runs
   `twine check --strict`, verifies the built version matches the tag, and uploads to PyPI.

The one-time PyPI setup and the TestPyPI rehearsal are documented in the repository's
[README](https://github.com/nghialuffy/tcbs-api#releasing).

A published version can **never** be re-uploaded, so bump `__version__` for every attempt —
including failed ones. The tag/version guard in the workflow catches the common slip of tagging a
version you forgot to bump.
