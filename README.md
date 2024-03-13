# Fastapi Tui <!-- omit in toc -->

This repository is a template for a basic Python project using
[Poetry](https://python-poetry.org/), with assorted Linting and Testing
libraries installed as standard. It also uses
[pre-commit](https://pre-commit.com/).

- [Development setup](#development-setup)
  - [Task Runner](#task-runner)
  - [Linting](#linting)
  - [Pre-commit](#pre-commit)
- [License](#license)
- [Credits](#credits)

## Development setup

Install the dependencies using Poetry:

```console
$ poetry install
```

Then, activate the virtual environment:

```console
$ poetry shell
```

Now, you can start to code the meat of your application.

### Task Runner

The task-runner [Poe the Poet](https://github.com/nat-n/poethepoet) is installed
as a development dependency which allows us to run simple tasks (similar to
`npm` scripts).

These are run (from within the virtual environment) using the `poe` command and
then the script name, for example:

```console
$ poe pre
```

See the [Task Runner](https://py-maker.seapagan.net/tasks/) section in the
documentation for more details and a list of available tasks.

These are defined in the `pyproject.toml` file in the `[tool.poe.tasks]`
section. Take a look at this file if you want to add or remove tasks.

### Linting

The generated project includes
[Ruff](https://docs.astral.sh/ruff/){:target="_blank"} for linting and code
style formatting. [Mypy](http://mypy-lang.org/){:target="_blank"} is installed
for type checking. These are set quite strictly by default, but you can edit the
tools configuration in the `pyproject.toml` file.

### Pre-commit

There is a [pre-commit](https://pre-commit.com/) configuration provided to run
some checks on the code before it is committed.  This is a great tool to help
keep your code clean.

To install pre-commit, run the following command from inside your venv:

```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

## License

This project is released under the terms of the MIT license.

## Credits

The original Python boilerplate for this package was created using
[Pymaker](https://github.com/seapagan/py-maker) by [Grant
Ramsay](https://github.com/seapagan)
