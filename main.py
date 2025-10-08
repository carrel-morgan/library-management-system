from fastapi import FastAPI

app = FastAPI()
print("Hello from library-management-system!")

@app.get("/")
async def root():
    return {"message": "Hello, User."}
