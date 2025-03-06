import uvicorn
import sys
from dotenv import load_dotenv
from app.main import app
from app.core.config import settings

# load env
load_dotenv()

def main():
    """
    main function to start FastAPI application
    """
    # print startup information
    print(f"Application Name: {settings.APP_NAME}")
    print(f"Starting FastAPI application - Listening on: {settings.HOST}:{settings.PORT}")
    print(f"API Documentation URL: http://{settings.HOST if settings.HOST != '0.0.0.0' else 'localhost'}:{settings.PORT}/docs")
    print(f"Debug Mode: {'Enabled' if settings.DEBUG else 'Disabled'}")
    
    # run app
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )

if __name__ == "__main__":
    main() 