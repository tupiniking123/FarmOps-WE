from __future__ import annotations

import atexit
import logging
import signal
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

import requests

PORT = 8501
URL = f"http://localhost:{PORT}"
PROCESS: subprocess.Popen[str] | None = None


def base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def app_path() -> Path:
    return base_dir() / "client" / "app.py"


def setup_logging() -> None:
    log_dir = base_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_dir / "app.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def wait_for_server(timeout: int = 60) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            response = requests.get(URL, timeout=1)
            if response.ok:
                return
        except requests.RequestException:
            pass
        time.sleep(1)
    raise TimeoutError("Streamlit não respondeu no tempo esperado.")


def terminate_streamlit(*_: object) -> None:
    global PROCESS
    if PROCESS and PROCESS.poll() is None:
        logging.info("Encerrando processo do Streamlit...")
        PROCESS.terminate()
        try:
            PROCESS.wait(timeout=10)
        except subprocess.TimeoutExpired:
            PROCESS.kill()
    PROCESS = None


def start_streamlit() -> subprocess.Popen[str]:
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path()),
        "--server.port",
        str(PORT),
        "--server.headless",
        "true",
    ]
    logging.info("Iniciando Streamlit: %s", " ".join(cmd))
    return subprocess.Popen(
        cmd,
        cwd=base_dir(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        creationflags=creationflags,
    )


def main() -> int:
    global PROCESS
    setup_logging()
    if not app_path().exists():
        logging.error("App não encontrado em %s", app_path())
        return 1

    atexit.register(terminate_streamlit)
    signal.signal(signal.SIGINT, terminate_streamlit)
    signal.signal(signal.SIGTERM, terminate_streamlit)

    try:
        PROCESS = start_streamlit()
        wait_for_server()
        logging.info("Abrindo navegador em %s", URL)
        webbrowser.open(URL)

        while PROCESS.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Interrupção recebida pelo usuário.")
    except Exception as exc:  # noqa: BLE001
        logging.exception("Erro no launcher: %s", exc)
        return 1
    finally:
        terminate_streamlit()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
