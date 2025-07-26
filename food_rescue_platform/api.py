
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from models.database import Database
from models.food_item import FoodItem as FoodItemModel

app = FastAPI()
db = Database()

class FoodItem(BaseModel):
    item_id: int
    name: str
    quantity: int
    expiry_date: str
    location: str
    donor_id: int
    is_claimed: bool = False
    recipient_id: Optional[int] = None

class DonationRequest(BaseModel):
    name: str
    quantity: int
    expiry_date: str
    location: str
    donor_id: int

class ClaimRequest(BaseModel):
    item_id: int
    recipient_id: int

@app.post("/donate", response_model=FoodItem)
def donate_food(req: DonationRequest):
    item_id = db.food_items.count_documents({}) + 1
    food_item = FoodItemModel(
        item_id=item_id,
        name=req.name,
        quantity=req.quantity,
        expiry_date=req.expiry_date,
        donor_id=req.donor_id,
        location=req.location
    )
    db.add_food_item(food_item.to_dict())
    return FoodItem(**food_item.to_dict())

@app.get("/food", response_model=List[FoodItem])
def list_food():
    items = db.food_items.find()
    food_list = []
    for item in items:
        # Remove MongoDB _id and fill missing fields with defaults
        item = dict(item)
        item.pop('_id', None)
        food = {
            'item_id': int(item.get('item_id', 0)),
            'name': item.get('name', ''),
            'quantity': int(item.get('quantity', 0)),
            'expiry_date': item.get('expiry_date', ''),
            'location': item.get('location', ''),
            'donor_id': int(item.get('donor_id', 0)),
            'is_claimed': bool(item.get('is_claimed', False)),
            'recipient_id': item.get('recipient_id', None)
        }
        food_list.append(FoodItem(**food))
    return food_list

@app.post("/claim", response_model=FoodItem)
def claim_food(req: ClaimRequest):
    result = db.food_items.update_one(
        {"item_id": req.item_id, "is_claimed": False},
        {"$set": {"is_claimed": True, "recipient_id": req.recipient_id}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Food item not found or already claimed")
    item = db.food_items.find_one({"item_id": req.item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Food item not found after update")
    item = dict(item)
    item.pop('_id', None)
    food = {
        'item_id': int(item.get('item_id', 0)),
        'name': item.get('name', ''),
        'quantity': int(item.get('quantity', 0)),
        'expiry_date': item.get('expiry_date', ''),
        'location': item.get('location', ''),
        'donor_id': int(item.get('donor_id', 0)),
        'is_claimed': bool(item.get('is_claimed', False)),
        'recipient_id': item.get('recipient_id', None)
    }
    return FoodItem(**food)

@app.get("/report/summary")
def report_summary():
    total_donated = db.food_items.count_documents({})
    total_claimed = db.food_items.count_documents({"is_claimed": True})
    return {"total_donated": total_donated, "total_claimed": total_claimed}
