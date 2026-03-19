from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize the limiter with IP address based tracking
limiter = Limiter(key_func=get_remote_address)

# We will apply this to the route
