from fastapi import FastAPI

app = FastAPI(title="Versions API")


@app.get("/")
def home():
    return {"Server running": True}
