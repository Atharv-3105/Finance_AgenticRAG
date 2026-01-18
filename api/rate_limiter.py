import time 
from fastapi import Request, HTTPException

REQUEST_LOG = {}
RATE_LIMIT = 30 

async def rate_limiter(request: Request):
    ip = request.client.host 
    now = time.time()
    
    REQUEST_LOG.setdefault(ip, [])
    REQUEST_LOG[ip] = [t for t in REQUEST_LOG[ip] if now - t < 60]
    
    if len(REQUEST_LOG[ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail = "Too many request, slow down"
        )
        
    REQUEST_LOG[ip].append(now)