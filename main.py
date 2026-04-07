"""Main module with FastAPI application."""

from typing import Optional

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Simple API", description="Practice API", version="1.0.0")


class Item:
    """Item model class."""

    def __init__(self, item_id: int, name: str, price: float, description: Optional[str] = None):
        """Initialize item."""
        self.id = item_id
        self.name = name
        self.price = price
        self.description = description


# In-memory storage
items_db = {}


@app.get("/")
def read_root() -> dict:
    """Root endpoint."""
    return {"message": "Welcome to the API"}


@app.post("/items/{item_id}")
def create_item(item_id: int, name: str, price: float, description: Optional[str] = None) -> dict:
    """Create a new item."""
    if item_id in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")

    items_db[item_id] = Item(item_id, name, price, description)
    return {"message": "Item created", "item_id": item_id}


@app.get("/items/{item_id}")
def get_item(item_id: int) -> dict:
    """Get an item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items_db[item_id]
    return {"id": item.id, "name": item.name, "price": item.price, "description": item.description}


@app.get("/items")
def get_all_items() -> list:
    """Get all items."""
    return [{"id": item.id, "name": item.name, "price": item.price, "description": item.description}
            for item in items_db.values()]


@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float, description: Optional[str] = None) -> dict:
    """Update an existing item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db[item_id] = Item(item_id, name, price, description)
    return {"message": "Item updated", "item_id": item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict:
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"message": "Item deleted", "item_id": item_id}
