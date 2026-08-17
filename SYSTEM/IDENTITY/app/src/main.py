from fastapi import FastAPI

app = FastAPI(
    title="CENCOM IDENTITY",
    description="Hệ thống quản lý tài khoản và phân quyền CENCOM",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "system": "CENCOM IDENTITY",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }