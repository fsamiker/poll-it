from datetime import datetime

def is_isoformat(date_str):
    try:
        datetime.fromisoformat(date_str).replace('Z', '+00:00')
    except:
        return False
    return True