# Machine Dialect Runner

A FastAPI server that provides an HTTP API for executing [Machine Dialect™](https://pypi.org/project/machine-dialect/) code. Machine Dialect™ is a natural language programming language that allows you to write code in Markdown format.

## Features

- 🚀 **REST API**: Simple HTTP endpoints for code execution
- 🛡️ **Error Handling**: Comprehensive error handling and validation
- 🔍 **Debug Mode**: Optional debug information for troubleshooting
- 📚 **Interactive Docs**: Auto-generated OpenAPI documentation
- ⚡ **Fast**: Built with FastAPI for high performance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kennylajara/machine-dialect-runner.git
cd machine-dialect-runner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
python main.py
```

The server will start on `http://localhost:8000` by default.

### API Endpoints

#### `POST /execute`

Execute Machine Dialect™ code.

**Request Body:**
```json
{
  "code": "Define `x` as number.\nSet `x` to _42_.",
  "debug": false
}
```

**Response:**
```json
{
  "success": true,
  "result": "Execution completed successfully",
  "error": null,
  "debug_info": null
}
```

#### `GET /`

Get API information.

#### `GET /health`

Health check endpoint.

### Example Usage

#### Using curl:

```bash
# Simple execution
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{"code":"Define `x` as number.\nSet `x` to _42_."}'

# With debug mode
curl -X POST "http://localhost:8000/execute" \
  -H "Content-Type: application/json" \
  -d '{"code":"Define `result` as number.\nSet `result` to _100_.","debug":true}'
```

#### Using Python requests:

```python
import requests

response = requests.post(
    "http://localhost:8000/execute",
    json={
        "code": "Define `x` as number.\nSet `x` to _42_.",
        "debug": False
    }
)

result = response.json()
print(result)
```

## Machine Dialect™ Syntax Examples

Machine Dialect™ uses natural language constructs in Markdown. Here are some examples:

### Basic Variables
```markdown
Define `x` as number.
Set `x` to _42_.
```

### Conditional Logic
```markdown
Define `temperature` as number.
Set `temperature` to _25_.

If `temperature` > _20_ then:
> Set `status` to "warm".
```

### Functions
```markdown
Define function `add` with parameters `a` as number and `b` as number returns number:
> Return `a` + `b`.
```

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## Error Handling

The API provides detailed error messages for:
- Compilation errors in Machine Dialect™ code
- Runtime execution errors
- Invalid request formats
- Server errors

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Dependencies

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [machine-dialect](https://pypi.org/project/machine-dialect/) - Machine Dialect™ compiler and runtime
- [Pydantic](https://pydantic.dev/) - Data validation
- [Uvicorn](https://www.uvicorn.org/) - ASGI server

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
