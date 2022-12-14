# Binocular

[![PyPI](https://img.shields.io/pypi/v/binocular.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/binocular.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/binocular)][pypi status]
[![License](https://img.shields.io/pypi/l/binocular)][license]

[![Read the documentation at https://binocular.readthedocs.io/](https://img.shields.io/readthedocs/binocular/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/MSAdministrator/binocular/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/MSAdministrator/binocular/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/binocular/
[read the docs]: https://binocular.readthedocs.io/
[tests]: https://github.com/MSAdministrator/binocular/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/MSAdministrator/binocular
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

This project aims to provide a singlur way for detection engineers to research and identify if any number of indicators are known by both threat intelligence and customers.

## Current Features

- Extracts IOCs from a given string
- Create or update configuration file containing secret API keys
    - Default path is `~/.config/binocular.yml`
- Lookup URLs in VirusTotal and urlscan.io
- Lookup domains, md5, sha1, and sha256 hashes in VirusTotal

## Requirements

- TODO

## Installation

You can install _Binocular_ via [pip] from [PyPI]:

```console
$ pip install binocular
```

It is preferred that you use `poetry` when developing `binocular`.

```
poetry install
poetry run binocular magnify "some string"
poetry run binocular get_config
poetry run binocular update_config
```

## Usage

Please see the [Command-line Reference] for details.

```
binocular magnify "string"
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

You can run all the pre-commit hooks by running

```
poetry run pre-commit run --all-files
```

## License

Distributed under the terms of the [MIT license][license],
_Binocular_ is free and open source software.

## Security

Security concerns are a top priority for us, please review our [Security Policy](SECURITY.md).

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@MSAdministrator]'s [Hypermodern Python Cookiecutter] template.

[@MSAdministrator]: https://github.com/MSAdministrator
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/MSAdministrator/binocular/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/MSAdministrator/binocular/blob/main/LICENSE
[contributor guide]: https://github.com/MSAdministrator/binocular/blob/main/CONTRIBUTING.md
[command-line reference]: https://binocular.readthedocs.io/en/latest/usage.html
