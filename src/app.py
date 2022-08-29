from fastapi import FastAPI
from routes.users import router
from docs import tags_metadata

app = FastAPI(
    title = "REST API with FastAPI and MongoDB - CRUD",
    description = "This is a simple REST API with FastAPI using MongoDB.",
    version = "0.0.1",
    openapi_tags = tags_metadata
)

#Incluir rutas a la app
app.include_router(router)