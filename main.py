import uvicorn
from fastapi import FastAPI
from routers.files import router

app = FastAPI(
    title="OCR API", openapi_url="/openapi.json"
)

app.include_router(router, prefix='/files')

if __name__ == "__main__":
    app_port = int(os.getenv("APP_PORT"))
    uvicorn.run(app, host="0.0.0.0", port=app_port, log_level="debug")
