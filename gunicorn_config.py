# Gunicorn Configuration File
# Usage: gunicorn -c gunicorn_config.py Kart.wsgi:application

import multiprocessing
import os
from pathlib import Path

# Server socket configuration
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1  # Recommended formula
worker_class = "sync"  # Use "gevent" for async
worker_connections = 1000
timeout = 30
keepalive = 2

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "shopping-kart"

# Server hooks (optional)
def on_starting(server):
    print("Gunicorn server is starting...")

def when_ready(server):
    print("Gunicorn server is ready. Spawning workers.")

def on_exit(server):
    print("Gunicorn server has exited.")

# SSL (if using Gunicorn with SSL directly)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
# ssl_version = ssl.PROTOCOL_TLSv1_2
# ciphers = "TLSv1"

# Headers
forwarded_allow_ips = "*"
secure_scheme_headers = {
    "X_PROTO": "https",
    "X_FORWARDED_PROTOCOL": "https",
    "X_FORWARDED_PROTO": "https",
    "X_FORWARDED_SSL": "on",
    "X_URL_SCHEME": "https",
}
