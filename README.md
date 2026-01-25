# gakoway

`gakoway` is a dynamic API Gateway designed to clone, prepare, and serve Python-based services from remote repositories or local directories. It routes HTTP requests directly to Python functions within those services, supporting hot-reloading and automatic dependency management.

## Features

- **Dynamic Service Loading**: Clone services from GitHub or use local directories on the fly.
- **Function Routing**: Map HTTP requests to Python functions using the pattern `/<module>/<file>/<function>`.
- **Automatic Dependency Management**: Automatically installs dependencies from `requirements.txt`, `pyproject.toml`, or `setup.py` when a service is loaded.
- **Hot Reloading**: Reflect changes in service code without restarting the gateway.
- **JSON Support**: Native handling of JSON requests and responses.
- **Container Ready**: Includes a `Dockerfile` for easy deployment.

## Installation

### Prerequisites

- Python
- Git
- Virtual Environment (required for `cli.py`)

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/youruser/gakoway.git
   cd gakoway
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install .
   ```

## Usage

### Starting a Service

Use the `cli.py` tool to clone a repository and start the gateway:

```bash
python cli.py https://github.com/example/my-service-repo
```

The CLI will:
1. Extract the repository name.
2. Clone the repository (or pull if it already exists).
3. Install any dependencies found in the repository.
4. Start the `gateway.py` server.

### API Routing

Once the gateway is running, it routes requests based on the URL path:

`http://localhost:5000/<module>/<file>/<function>`

- `module`: The directory name of the service (e.g., the cloned repository name).
- `file`: The Python file name (without `.py`) within that module.
- `function`: The name of the function to call.

#### Example

If you have a service `my_service` with a file `utils.py` containing:

```python
def add_numbers(a, b):
    return {"result": a + b}
```

You can call it via POST:

```bash
curl -X POST http://localhost:5000/my_service/utils/add_numbers \
     -H "Content-Type: application/json" \
     -d '{"a": 5, "b": 10}'
```

Response:
```json
{"result": 15}
```

## Docker

You can also run `gakoway` using Docker:

1. Build the image:
   ```bash
   docker build -t gakoway .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 gakoway
   ```

The gateway will be available at `http://localhost:8000`.

## License

MIT
