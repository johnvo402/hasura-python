from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Hasura-Integrator")

app.include_router(router)
