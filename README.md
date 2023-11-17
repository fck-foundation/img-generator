# Image Generator API

This is a simple API that generates images with information about crypto currencies.

- API version: 1.0.0

## Requirements.

* Python >= 3.12
* poetry >= 1.7.1

## Installation & Usage

To run the server, please execute the following from the root directory:

```bash
poetry install
poetry run uvicorn src.WidgetGen.main:app --reload
```

and open your browser at `http://localhost:8000/docs/` to see the docs.

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
docker build -t imggenerator .
docker run --rm --name imggenerator -p 8000:80 imggenerator
```

## Tests

>TBD
