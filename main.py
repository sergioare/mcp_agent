from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import meta, upload, embed, search, JSON_RCP

app = FastAPI(title="Landing Agent MCP Server")

app.include_router(meta.router)
app.include_router(upload.router)
app.include_router(embed.router)
app.include_router(search.router)
app.include_router(JSON_RCP.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Landing Agent MCP Server running"}
