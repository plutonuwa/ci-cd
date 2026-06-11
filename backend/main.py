from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

CORS_ORIGINS = ["*"]  # Allow all origins for simplicity, adjust as needed
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS)

class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    price: float

LocalStage = [Item(name="Item 1", price=10.0), Item(name="Item 2", price=20.0), Item(name="Item 3", price=30.0), Item(name="Item 4", price=40.0), Item(name="Item 5", price=50.0)]

@app.get("/")
def read_root():
    return {"status": "success", "message": "Hello World"}

@app.get("/items")
def read_items():
    return {"status": "success", "data": LocalStage, "count": len(LocalStage)}


@app.post("/items", status_code=201)
def create_item(item: Item):
    LocalStage.append(item)
    return {"status": "success", "data": item}

@app.get("/items/{item_id}")
def read_item(item_id: UUID):
    for item in LocalStage:
        if item.id == item_id:
            return {"status": "success", "data": item}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
