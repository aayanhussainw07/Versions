from fastapi import FastAPI

app = FastAPI(title = "Versions API")

@app.get("/health")
def health():
    return {"ok": True}