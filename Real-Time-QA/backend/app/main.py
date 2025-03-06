from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import websocket_router
from app.services.chat_service import chat_service
from app.core.config import settings
from app.core.response import server_error, success_response
from app.utils.logger import logger
import os
from pathlib import Path

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    description="Web application based on FastAPI with integrated DIFY chat functionality. Provides HTTP API and WebSocket real-time chat services.",
    version="0.1.0",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Chat",
            "description": "DIFY chat API, including chat completion and simple Q&A interfaces"
        },
        {
            "name": "WebSocket Chat",
            "description": "WebSocket real-time chat interface, supporting peer-to-peer communication"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Add WebSocket middleware
class WebSocketMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Skip logging for WebSocket requests
        if request.url.path.startswith("/ws/"):
            # WebSocket request, don't log details
            return await call_next(request)
        else:
            # Regular HTTP request, can log
            logger.debug(f"HTTP request: {request.method} {request.url.path}")
            response = await call_next(request)
            return response

# Add middleware
app.add_middleware(WebSocketMiddleware)

# Set static files directory
static_dir = Path(__file__).parent.parent / "static"
if not static_dir.exists():
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Set templates directory
templates_dir = Path(__file__).parent.parent / "templates"
if not templates_dir.exists():
    os.makedirs(templates_dir)
templates = Jinja2Templates(directory=templates_dir)

# Application startup event
@app.on_event("startup")
async def startup_event():
    """Executed when the application starts"""
    logger.info(f"Starting application: {settings.APP_NAME}")
    logger.info(f"Server address: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"API documentation: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"WebSocket chat page: http://{settings.HOST}:{settings.PORT}/chat")
    
    # Check log directory
    from app.utils.logger import LOG_DIR
    logger.info(f"Log files saved at: {LOG_DIR}")
    
    # Check necessary environment variables
    if not settings.DIFY_API_KEY:
        logger.warning("DIFY_API_KEY not set, API calls will fail")
    
    if not settings.DIFY_API_URL:
        logger.warning("DIFY_API_URL not set, using default URL")
    
    # Validate API connection
    try:
        # Simple test request
        test_messages = [{"role": "user", "content": "Hello"}]
        await chat_service.chat_completion(
            messages=test_messages,
            max_tokens=10
        )
        logger.info("Dify API connection successful")
    except Exception as e:
        logger.error(f"Dify API connection failed: {str(e)}")
        # Don't interrupt application startup, but log the error
        
    # Record mock mode status
    if settings.MOCK_MODE:
        logger.warning("Application running in mock mode, will not call actual DIFY API")

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Executed when the application shuts down"""
    logger.info(f"Shutting down application: {settings.APP_NAME}")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=server_error(message=f"Internal server error: {str(exc)}")
    )

# Register routes
app.include_router(websocket_router.router)

@app.get("/")
async def root():
    """Root route"""
    return success_response(
        data={"version": "0.1.0", "docs_url": "/docs", "chat_url": "/chat"},
        message="Welcome to my FastAPI application. You can view API documentation at /docs or use the chat feature at /chat"
    )