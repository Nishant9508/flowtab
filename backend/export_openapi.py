import json
from app.main import app
from fastapi.openapi.utils import get_openapi

def export():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )
    with open("../docs/api.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)

if __name__ == "__main__":
    export()
