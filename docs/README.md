# Translation API

This project provides an API for translating text using state-of-the-art AI models. Translate using Facebook/Meta's mBART or Seamless models.

## Features

- **RESTful API**: Exposes RESTful API endpoints
- **Translation**: Translates text using translation models like Facebook/Meta's mBART and Seamless
- **Configuration**: The repository includes a `.env` file that defines configurable environment variables.
- **Memory Optimization**: Models are loaded in separate processes and terminated after a configurable idle timeout to conserve RAM

## Available Distributions

### Docker Images

Available on [Docker Hub](https://hub.docker.com/r/ggwozdz/translation-api):

- `version-cpu`: CPU-only version (fully tested and stable)
- `version-cuda124`: NVIDIA CUDA 12.4 support for GPU acceleration (proof-of-concept implementation)*
- `version-rocm62`: AMD ROCm 6.2 support for GPU acceleration (proof-of-concept implementation, requires build from source code)*
- `latest`: Points to latest CPU version

*Note on GPU Support: The current implementations of CUDA and ROCm support are provided as proof-of-concept solutions. While these implementations handle basic scenarios effectively, they haven't undergone comprehensive testing across all use cases. Users planning to utilize GPU acceleration may need to modify the Docker images to include additional environment-specific GPU support software. I recommend using the CPU version, which has been thoroughly tested and validated. The GPU implementations serve as a foundation for future development of more sophisticated functionality.

### Windows Executable

Download the CPU version executable from [GitHub Releases](https://github.com/ggwozdz90/translation-api/releases).

## Quick Start

### Prerequisites

Choose your preferred distribution:

- **Windows Executable**:
  - Windows 10 or later

- **Docker Images**:
  - [Docker](https://www.docker.com/get-started/)

### Using Docker

- Run the following command to start the API server:

    ```bash
    docker run -d -p 8000:8000 \
      -e LOG_LEVEL=INFO \
      -e DEVICE=cpu \
      -e FASTAPI_HOST=0.0.0.0 \
      -e FASTAPI_PORT=8000 \
      -e MODEL_IDLE_TIMEOUT=60 \
      -e TRANSLATION_MODEL_NAME=facebook/mbart-large-50-many-to-many-mmt \
      -e TRANSLATION_MODEL_DOWNLOAD_PATH=downloaded_translation_models \
      -v ./volume/downloaded_translation_models:/app/downloaded_translation_models \
      ggwozdz/translation-api:latest
    ```

### Using Docker Compose

- Create a `docker-compose.yml` file with the following content and run `docker-compose up`:

    ```yaml
    services:
      api:
        image: ggwozdz/translation-api:latest
        environment:
          - LOG_LEVEL=INFO
          - DEVICE=cpu
          - FASTAPI_HOST=0.0.0.0
          - FASTAPI_PORT=8000
          - MODEL_IDLE_TIMEOUT=60
          - TRANSLATION_MODEL_NAME=facebook/mbart-large-50-many-to-many-mmt
          - TRANSLATION_MODEL_DOWNLOAD_PATH=downloaded_translation_models
        ports:
          - "8000:8000"
        volumes:
          - ./volume/downloaded_translation_models:/app/downloaded_translation_models
    ```

### Using Windows Executable

1. Download from GitHub Releases
2. Run `translation-api.exe`

## API Features

### Translate Text

- Request:

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/translate' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "text_to_translate": "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.",
      "source_language": "en_US",
      "target_language": "pl_PL",
      "generation_parameters": { "max_length": 10240, "num_beams": 10 }
    }'
    ```

- Response:

    ```json
    {
      "translation": "Wieża Eiffla ma wysokość 324 metrów, mniej więcej taką samą wysokość jak 81-piętrowy budynek, i jest najwyższą budowlą w Paryżu. Jego podstawa jest kwadratowa, mierząc 125 metrów na każdej stronie. Podczas jej budowy Wieża Eiffla przekroczyła Pomnik Waszyngtonu, stając się najwyższą budowlą stworzoną przez człowieka na świecie, tytuł utrzymywał przez 41 rok, dopóki budynek Chrysler w Nowym Jorku nie został ukończony w 1930 roku."
    }
    ```

#### Generation parameters

The `generation_parameters` field in the request body allows you to specify the parameters which are described in the model documentation.

[For Seamless model](https://huggingface.co/docs/transformers/main/en/model_doc/seamless_m4t#transformers.SeamlessM4TForTextToText.generate) and [for mBART model](https://huggingface.co/docs/transformers/main/en/model_doc/mbart#transformers.MBartForConditionalGeneration.generate)

### Health Check

- Request:

    ```bash
    curl -X GET "http://localhost:8000/healthcheck"
    ```

- Response:

    ```json
    {
      "status": "OK"
    }
    ```

## Configuration

The application uses a `.env` file or Docker Compose to define configurable environment variables. Below are the available configuration options:

- `LOG_LEVEL`: The logging level for the application. Supported levels are `NOTSET`, `DEBUG`, `INFO`, `WARN`, `WARNING`, `ERROR`, `FATAL`, and `CRITICAL`. The same log level will be applied to `uvicorn` and `uvicorn.access` loggers. Default is `INFO`.
- `DEVICE`: Device to run the models on (`cpu` or `cuda`). Default is `cpu`.
- `FASTAPI_HOST`: Host for the FastAPI server. Default is `127.0.0.1`.
- `FASTAPI_PORT`: Port for the FastAPI server. Default is `8000`.
- `TRANSLATION_MODEL_NAME`: Name of the translation model to use. Supported models are `facebook/mbart-large-50-many-to-many-mmt` and `facebook/seamless-m4t-v2-large`. Default is `facebook/seamless-m4t-v2-large`.
- `TRANSLATION_MODEL_DOWNLOAD_PATH`: Path where translation models are downloaded. Default is `downloaded_translation_models`.
- `MODEL_IDLE_TIMEOUT`: Time in seconds after which the model will be unloaded if not used. Default is `60`.

## Supported Languages

Refer to mapping files in source code for supported languages:

- mBART: [mbart_mapping.json](../src/assets/mappings/mbart_mapping.json)
- Seamless: [seamless_mapping.json](../src/assets/mappings/seamless_mapping.json)

## Developer Guide

Developer guide is available in [docs/DEVELOPER.md](DEVELOPER.md).

## Table of Contents

- [Translation API](#translation-api)
  - [Features](#features)
  - [Available Distributions](#available-distributions)
    - [Docker Images](#docker-images)
    - [Windows Executable](#windows-executable)
  - [Quick Start](#quick-start)
    - [Prerequisites](#prerequisites)
    - [Using Docker](#using-docker)
    - [Using Docker Compose](#using-docker-compose)
    - [Using Windows Executable](#using-windows-executable)
  - [API Features](#api-features)
    - [Translate Text](#translate-text)
      - [Generation parameters](#generation-parameters)
    - [Health Check](#health-check)
  - [Configuration](#configuration)
  - [Supported Languages](#supported-languages)
  - [Developer Guide](#developer-guide)
  - [Table of Contents](#table-of-contents)
