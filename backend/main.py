from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

app = FastAPI()

class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    price: float

LocalStage = [Item(name="Item 1", price=10.0), Item(name="Item 2", price=20.0)]

@app.get("/")
def read_root():
    return {"status": "success", "message": "Hello World"}

@app.get("/items")
def read_items():
    return {"status": "success", "data": LocalStage}


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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)