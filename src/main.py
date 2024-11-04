# src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.routes import product_lookup, image_product_lookup, shopify_sync

app = FastAPI()

# Allow all origins, or specify allowed origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["https://your-streamlit-app-url.com"] in production for specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include the routes
app.include_router(product_lookup.router, prefix="/api/v1")
app.include_router(image_product_lookup.router, prefix="/api/v1")
app.include_router(shopify_sync.router, prefix="/api/v1")