from datetime import datetime
from typing import Dict, Any

class SessionManager:
    """
    In-memory session tracker for API requests.
    Tracks requests by IP address with timestamp and count.
    """
    def __init__(self):
        # We store ips as keys, values are dicts with count, timestamp
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def track_request(self, ip_address: str):
        """
        Increment the request count and update the last seen timestamp
        for the given IP address.
        """
        now = datetime.now()
        
        if ip_address in self.sessions:
            self.sessions[ip_address]["count"] += 1
            self.sessions[ip_address]["timestamp"] = now.isoformat()
        else:
            self.sessions[ip_address] = {
                "count": 1,
                "timestamp": now.isoformat()
            }

session_manager = SessionManager()
