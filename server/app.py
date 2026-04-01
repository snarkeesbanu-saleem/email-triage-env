from fastapi import FastAPI
from openenv.core.env_server import create_fastapi_app

# Use the existing Echo models and environment (this will make the server start)
from models import EchoAction, EchoObservation
from echo_environment import EchoEnv

def create_app():
    """Create FastAPI app for OpenEnv - Scaler x Meta Hackathon"""
    
    env = EchoEnv()   # Using Echo for now (safe for deployment)

    app = create_fastapi_app(
        env=env,
        action_class=EchoAction,
        observation_class=EchoObservation,
        title="Email Triage Environment (Echo) - Scaler x Meta Hackathon",
        description="Basic Echo Environment for testing OpenEnv deployment. Will be upgraded to Email Triage.",
        version="0.2.0",
        max_concurrent_envs=32,
        supports_concurrent_sessions=True,
    )

    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "environment": "email-triage-env (echo mode)",
            "message": "Server is running. Ready for deployment check."
        }

    return app


# Main app instance
app = create_app()


# Allow running with: uv run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )