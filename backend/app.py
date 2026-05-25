from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_user():
    return "Hello from Effective Mobile!"

@app.get("/health")
def health():
    return {"status": "ok"}