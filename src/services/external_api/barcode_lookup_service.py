# src/services/barcode_lookup_service.py

import urllib.request
import json
import os

# Load the API key from environment variables
BARCODE_LOOKUP_API_KEY = os.getenv("BARCODE_LOOKUP_API_KEY","kzpnb1nnxcto8t079a33gsumty9pd2")

def lookup_product_by_barcode(barcode: str):
    """
    Fetches complete product details by barcode from the Barcode Lookup API.
    """
    try:
        url = f"https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key={BARCODE_LOOKUP_API_KEY}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        print(f"Barcode Response -> {data}")
        if len(data["products"]) > 0:
            # Return the full product dictionary
            return data["products"][0]
        else:
            return {"error": "Product not found"}
    except Exception as e:
        raise Exception(f"Error fetching product data: {e}")

