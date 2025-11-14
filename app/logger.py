import time
from datetime import datetime

RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"

def log_info(msg):
    print(f"{GREEN}[INFO]{RESET} {msg}")

def log_debug(msg):
    print(f"{CYAN}[DEBUG]{RESET} {msg}")

def log_warn(msg):
    print(f"{YELLOW}[WARN]{RESET} {msg}")

def log_section(label):
    print(f"\n{MAGENTA}==== {label} ===={RESET}\n")

def timed(func):
    """Measure how long a function call took."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start) * 1000
        log_debug(f"{func.__name__} took {duration:.2f} ms")
        return result
    return wrapper
