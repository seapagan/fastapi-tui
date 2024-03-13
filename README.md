# Fastapi Tui <!-- omit in toc -->

This is a work in progress to see how to use
[Textual](https://textual.textualize.io/) and
[FastAPI](https://fastapi.tiangolo.com/) together, and to see if it's possible
to create a TUI application that can communicate with a FastAPI server.

Right now there is no usable code here, but I'm working on it.

- [Development setup](#development-setup)
- [FastAPI server](#fastapi-server)
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

## FastAPI server

The project contains a very basic FastAPI server. You can run it directly using
the following command:

```console
$ uvicorn fastapi_tui.server:api --reload
```

There is a single endpoint at `/` that returns a JSON response with a message.
This server will be used initially to test the TUI application.

## License

This project is released under the terms of the MIT license.

## Credits

The original Python boilerplate for this package was created using
[Pymaker](https://github.com/seapagan/py-maker) by [Grant
Ramsay](https://github.com/seapagan)
