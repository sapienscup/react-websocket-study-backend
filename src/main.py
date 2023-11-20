from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .dependencies import get_token_header_dependency
from .internal import admin

# pylint: disable=no-name-in-module
from .routes import chat, graphql, health, todos

# pylint: enable=no-name-in-module

load_dotenv()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI(dependencies=[get_token_header_dependency])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(graphql.router)


@app.get("/")
async def root():
    html_content = """
    <html>
        <head>
            <title>Backend server</title>
        </head>
        <body>
            <h1>Server is running</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
