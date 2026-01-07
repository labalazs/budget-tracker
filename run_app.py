import subprocess
import sys
import time

def run_backend():
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--reload"
        ]
    )

def run_frontend():
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "frontend/streamlit_app.py"
        ]
    )

if __name__ == "__main__":
    print("Starting backend...")
    backend = run_backend()
    time.sleep(2)
    print("Starting frontend...")
    frontend = run_frontend()
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        backend.terminate()
        frontend.terminate()