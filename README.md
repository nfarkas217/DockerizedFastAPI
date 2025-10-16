# Dockerized FastAPI server

## Installation

### 1. Clone the repository

### 2. Install Docker

### 3. To run the projcet use the following command:

        'docker compose up --build'

## Endpoints

### 1. Health Check

**Endpoint:** `/health`

**Method:** `GET`

**Description:** Returns the status of the server-- 'ok' if the status of the server is ok and 'degraded' if not
Checks the disk, memory, cpu, and network of server
Reponse format example:

```json
{
  "status": "ok",
  "details": {
    "disk_percent": 0.8,
    "memory_percent": 9.7,
    "cpu_percent": 0,
    "network_ok": true
  }
}
```

---

### 2. Code Execution

**Endpoint:** `/run`

**Method:** `POST`

**Description:** Executes the provided Python code and returns the value of the variable `result` along with any logs from print statements within the code.

#### Request Format

```json
{
  "code": "<insert some python code>",
  "input_schema": <json object>,
  "output_schema": <json object>
}
```

**Note:** The `input_schema` and `output_schema` JSON objects are converted into Python dictionaries and appended to the start of the Python script before execution.

#### Response Format

```json
{
  "logs": "<insert results from print statements>",
  "result": <insert json object>
}
```

### example request body for /run

```json
{
  "code": "print('Input Schema: ', input_schema)\nprint('Output Schema: ', output_schema)\nresult = input_schema['a'] + output_schema['b']",
  "input_schema": {
    "a": 45
  },
  "output_schema": {
    "b": 7
  }
}
```

### curl command

```console
curl -X 'POST' \
 'http://0.0.0.0:8000/run' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -d '{
"code": "print('\''Input Schema: '\'', input_schema)\nprint('\''Output Schema: '\'', output_schema)\nresult = input_schema['\''a'\''] + output_schema['\''b'\'']",
"input_schema": {
"a": 45
},
"output_schema": {
"b": 7
}
}'
```

### response body

```json
{
  "result": 52,
  "logs": "full code: input_schema = {\"a\": 45}\noutput_schema = {\"b\": 7}\nprint('Input Schema: ', input_schema)\nprint('Output Schema: ', output_schema)\nresult = input_schema['a'] + output_schema['b']\nInput Schema: {'a': 45}\nOutput Schema: {'b': 7}\n"
}
```
