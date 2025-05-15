from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.routes import auth, users

# Init Limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Secure App")

# Intégration du Limiter dans l'app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Trusted Host
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1",],
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adapter au frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Limitation globale sur toutes les requêtes : 100 requêtes toutes les 15 minutes par IP
@app.middleware("http")
async def ddos_protection_middleware(request: Request, call_next):
    response = await limiter.limit("100/15minutes")(call_next)(request)
    return response

# Ajout de body size limit (ex : 1 MB)
@app.middleware("http")
async def body_size_limit_middleware(request: Request, call_next):
    if request.headers.get("content-length") and int(request.headers.get("content-length")) > 1024 * 1024:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=413, content={"detail": "Payload too large"})
    return await call_next(request)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
