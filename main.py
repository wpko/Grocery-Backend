from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

with open("data.json","r") as f:
    store_data = json.load(f)
    
cart = []

class CartItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/products")
def get_products():
    return store_data["products"]

@app.post("/cart/add")
def add_to_cart(item: CartItem):
    product = next((p for p in products if p["id"] == item.product_id), None)
    if product:
        cart.append({"name":product["name"],"quantity":item.quantity,"price":product["price"]})
    return {"message":f"{product['name']} added to cart"}

@app.get("/cart")
def view_cart():
    return{"cart": cart}

@app.post("/checkout")
def checkout():
    total = sum(item["price"] for item in cart)
    cart.clear()
    return {"message": "Checkout successful!", "total": total}
