from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from api import auth

app = FastAPI(title="Picolynne Store API")

app.include_router(auth.router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Picolynne Store API",
        version="1.0.0",
        description="Sistema de vendas com autenticação JWT",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi