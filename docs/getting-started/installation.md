# Installation

## Requirements

- Python 3.10 or newer
- A TCBS Open API key — obtain it from the [TCBS developer portal](https://developers.tcbs.com.vn/)

## With uv

```bash
uv add tcbs-api
```

## With pip

```bash
pip install tcbs-api
```

## From a source checkout

Either tool can install straight from the repository:

```bash
uv add git+https://github.com/nghialuffy/tcbs-api
pip install git+https://github.com/nghialuffy/tcbs-api
```

The library reads no config files and stores no state: it depends on `requests` and `pydantic`
only, with no async client, no retry layer and no token store — see
[Operational notes](../limitations.md#operational-notes). To work on the library itself, see
[Development](../development.md).

## Next

- [Quick start](quickstart.md)
- [API reference](../api/index.md)
