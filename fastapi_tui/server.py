"""A very basic API example."""

from fastapi import FastAPI

api = FastAPI()


@api.get("/")
def example() -> dict[str, str]:
    """Return a basic example."""
    return {"message": "Hello, World!"}
