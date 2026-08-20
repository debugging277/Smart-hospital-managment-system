"""
One-Click Launcher for Smart Hospital Management System
"""

import sys
import webbrowser
import threading
import time
import os

try:
    import uvicorn
except ImportError:
    print("Error: uvicorn is not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)


def open_browser():
    time.sleep(1.5)
    url = "http://127.0.0.1:8000"
    print(f"\n=======================================================")
    print(f"🏥 St. Metropolitan Smart Hospital Management System")
    print(f"🌐 Access Web Dashboard: {url}")
    print(f"📚 Interactive Swagger API Docs: {url}/docs")
    print(f"=======================================================\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
