from application.core.config import get_settings

if __name__ == "__main__":

    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "application.main:app",
        host="0.0.0.0",
        port=settings.app.project_port,
        reload=True,
    )
