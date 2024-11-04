from fastapi import APIRouter, HTTPException
import requests
import json
import os

# Set up the router
router = APIRouter()

# Shopify credentials (replace with your actual details or set as environment variables)
SHOPIFY_BASE_URL = os.getenv("SHOPIFY_BASE_URL", "https://your-development-store.myshopify.com")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "{access_token}")

@router.post("/shopify/sync")
async def sync_to_shopify(product_data: dict):
    """
    Sync product data to Shopify by creating a new product.
    """
    url = f"{SHOPIFY_BASE_URL}/admin/api/2024-01/products.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    # Structure the payload according to Shopify's API
    payload = {
        "product": {
            "title": product_data.get("title", ""),
            "body_html": f"<strong>{product_data.get('description', '')}</strong>",
            "vendor": product_data.get("manufacturer", ""),
            "product_type": product_data.get("category", ""),
            "status": "draft"  # Status can be "active" or "draft"
        }
    }

    try:
        # Make the API request to Shopify
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 201:
            return {"message": "Product synced successfully with Shopify!", "shopify_response": response.json()}
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to sync with Shopify: {response.json()}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error syncing with Shopify: {str(e)}")
