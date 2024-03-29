# Fastapi Tui <!-- omit in toc -->

This is a work in progress to see how to use
[Textual](https://textual.textualize.io/) and
[FastAPI](https://fastapi.tiangolo.com/) together, and to see if it's possible
to create a TUI application that can start/stop a FastAPI server and display the
logs in the TUI. This is primarily for development since you would not want to
run a FastAPI server in a TUI in production.

The code here works, but needs tidying up. The TUI application is very basic and
I have made no effort to optimize it, it's also my first Textual App so don't
expect too much :grin:

- [In Action](#in-action)
- [Development setup](#development-setup)
- [TUI application](#tui-application)
- [FastAPI server](#fastapi-server)
- [Further Plans](#further-plans)
- [License](#license)
- [Credits](#credits)

## In Action

![Example](media/screencast.gif)

## Development setup

Install the dependencies using Poetry:

```console
$ poetry install
```

Then, activate the virtual environment:

```console
$ poetry shell
```

## TUI application

You can run the application using the following command:

```console
$ fastapi-tui
```

The application allows you to start and stop the FastAPI server, and to display
(and clear) the log output in a separate panel.

## FastAPI server

The project contains a very basic FastAPI server. You can run it directly using
the following command:

```console
$ uvicorn fastapi_tui.server:api --reload
```

There is a single endpoint at `"/"` that returns a JSON response with a message.
This server will be used initially to test the TUI application. The "`/docs`"
and "`/redoc`" endpoints are also available for testing the FastAPI server.

## Further Plans

See the [TODO](TODO.md) file for a list of things I want to do next with this
project. The original idea was to see if I could create a TUI application that
could start/stop a FastAPI server and display the logs in the TUI, which I have
done. The next steps are to tidy up the code and to see if I can make the TUI
application more useful. Not sure how far I'll take this, but it's been a fun
experiment so far.

## License

This project is released under the terms of the MIT license.

## Credits

The original Python boilerplate for this package was created using
[Pymaker](https://github.com/seapagan/py-maker) by [Grant
Ramsay](https://github.com/seapagan) (Me! :grin:)
