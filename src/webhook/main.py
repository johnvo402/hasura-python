from fastapi import FastAPI
from .routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Hasura-Integrator")

origins = [
    "http://localhost:8080",
    "http://hasura:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Domain được phép
    allow_credentials=True,  # Cho phép cookie
    allow_methods=["*"],  # Cho phép mọi method (GET, POST, v.v.)
    allow_headers=["*"],  # Cho phép mọi header
)
app.include_router(router)
