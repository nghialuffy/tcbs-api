# Changelog

All notable changes to this project are documented in this file, following
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- **Breaking:** the write endpoints are gone (19 read-only operations remain) and the DTOs are pydantic v2 models.
- Every DTO field is described; the models follow live payloads where the document is wrong (see the README).

## [0.0.3] - 2026-09-21

- Every DTO carried exactly the fields `openapi-v1.0.0.json` declares, and import paths no longer repeat "dto".

## [0.0.2] - 2026-09-20

- Added the cash-market (5.x) and cash-statement (4.16) endpoints: 37 of the 44 operations.

## [0.0.1] - 2026-09-19

- Repackaged as `tcbs-api`: a declarative `pyproject.toml`, typed public API, MIT license, published to PyPI.
