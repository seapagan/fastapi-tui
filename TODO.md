# TODO

## TUI App

- add checkboxes for uvicorn options ie '--reload'.
- show the current process command line at the bottom under the logs.
- allow saving the log to a file. Ask for a file name, suggesting the current
  process name and the current date and time for example.
- set focus to the log after each button pressed as the button active highlight
  bugs me. **That would not be great for accessibility though**.
- maybe move the server status to the footer.
- add the ability to run a custom process, not just uvicorn.
- cancel autoscroll when the user scrolls up, reenable when the user scrolls to
  the bottom.
- add key bindings to toggle the server and to clear the logs.
- add color to the `status_code` at the end of the line (ie `200 OK` or `404 Not
  Found`).

## Docs

Document the application, working through and explaining the code. It took me a
few hours to get this to a working state and I think it would be useful to
document the process.

## Server

I may add a few more endpoints to the server to test the TUI application with
more complex responses.
