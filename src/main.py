# src/main.py

from fastapi import FastAPI
from src.api.v1.routes import product_lookup, image_product_lookup, shopify_sync

app = FastAPI()

# Include the routes
app.include_router(product_lookup.router, prefix="/api/v1")
app.include_router(image_product_lookup.router, prefix="/api/v1")
app.include_router(shopify_sync.router, prefix="/api/v1")