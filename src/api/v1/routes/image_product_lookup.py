# src/api/v1/routes/image_product_lookup.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from src.services.llm.google_gemini_service import describe_product_from_image
# from src.models.product_schema import Product, ProductDetails, ProductDimensions, ProductSpecifications
import typing_extensions as typing

router = APIRouter()

@router.post("/product/describe")
async def describe_product_image(image: UploadFile = File(...)):
    """
    Describes the product in the uploaded image using Google Gemini API.
    """
    try:
        # Save the uploaded image temporarily to a local path
        temp_image_path = Path(f"/tmp/{image.filename}")
        with open(temp_image_path, "wb") as buffer:
            buffer.write(await image.read())

        # Use the service layer to get product details from the image
        product_data = describe_product_from_image(temp_image_path)
        
        return {"status": "success", "product_data": product_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temp file after processing
        if temp_image_path.exists():
            temp_image_path.unlink()
