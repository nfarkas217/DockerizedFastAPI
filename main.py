from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psutil
import sys
import io
import traceback
import json
import socket

app = FastAPI()

def check_cpu_load(threshold = 90):
    cpu = psutil.cpu_percent(interval = 1)
    return cpu, cpu < threshold

def check_disk_usage(threshold = 90):
    disk = psutil.disk_usage('/')
    return disk.percent, disk.percent < threshold

def check_memory_usage(threshold = 90):
    mem = psutil.virtual_memory()
    return mem.percent, mem.percent < threshold

def check_network(host = "8.8.8.8", port = 53, timeout = 3):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        return True
    except Exception:
        return False

@app.get("/")
def read_root():
    return{"Hello": "World"}

@app.get("/health")
def health_check():
    disk_percent, disk_ok = check_disk_usage()
    mem_percent, mem_ok = check_memory_usage()
    cpu_percent, cpu_ok = check_cpu_load()
    network_ok = check_network()

    status = "ok" if all([disk_ok, mem_ok, cpu_ok, network_ok]) else "degraded"

    details = {
        "disk_percent": disk_percent,
        "memory_percent": mem_percent,
        "cpu_percent": cpu_percent,
        "network_ok": network_ok
    }

    return {
        "status": status,
        "details": details
    }

class RunRequest(BaseModel):
    code: str
    input_schema: dict
    output_schema: dict

@app.post("/run")
def run_code(request: RunRequest):

    try:
        # convert schemas to Python dict
        input_schema_str = f"input_schema = {json.dumps(request.input_schema)}\n"
        output_schema_str = f"output_schema = {json.dumps(request.output_schema)}\n"

        # prepend to code
        full_code = input_schema_str + output_schema_str + request.code
    except Exception as prep_error:
        raise HTTPException(
            status_code=400,
            detail=f"Error preparing code to execute: {str(prep_error)}"
        )

    # Prepare to capture print output
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    result = None
    error = None

    local_vars = {}

    try:
        # execute full code
        exec(full_code, {}, local_vars)
        result = local_vars.get('result', None)
    except Exception as e:
        error = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
    
    logs = mystdout.getvalue()

    response = {
        "result": result,
        "logs": logs
    }

    if error:
        response["error"] = error

    return response
