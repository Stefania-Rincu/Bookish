from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import auth
from app.controllers import bookish
from app.controllers import books

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.auth_controller.router)
app.include_router(bookish.router)
app.include_router(books.router)
