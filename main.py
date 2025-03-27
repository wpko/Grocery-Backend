from fastapi import FastAPI, HTTPException
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

with open("backend/data.json","r") as f:
    store_data = json.load(f)
    
cart = []

@app.get("/Products")
def get_products():
    return store_data["products"]

@app.post("/add-to-cart/{product_id}")
def add_to_cart(product_id: int):
    product = next((p for p in store_data["products"] if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    cart.append(product)
    return {"message":f"{product['name']} added to cart"}

@app.get("/cart")
def view_cart():
    return{"cart": cart}

@app.post("/checkout")
def checkout():
    total = sum(item["price"] for item in cart)
    cart.clear()
    return {"message": "Checkout successful!", "total": total}