import os

def is_pro() -> bool:
    token = os.getenv("NEONCRIPTO_PRO_TOKEN", "").strip()
    return len(token) >= 24
