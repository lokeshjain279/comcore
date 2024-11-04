# src/api/v1/routes/product_lookup.py

from fastapi import APIRouter, HTTPException
from src.services.external_api.barcode_lookup_service import lookup_product_by_barcode

router = APIRouter()

@router.get("/product/lookup/{barcode}")
async def product_lookup(barcode: str):
    """
    Looks up product details by barcode.
    """
    try:
        product_data = lookup_product_by_barcode(barcode)
        if product_data:
            return {"status": "success", "product_data": product_data}
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
