from fastapi import FastAPI

app = FastAPI(title="Showstock", description="Nutrition management for show livestock")

@app.get("/")
async def root():
    return {"message": "Welcome to Showstock - Nutrition management for show livestock"}

@app.get("/health")
async def health():
    return {"status": "healthy"}