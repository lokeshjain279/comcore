# src/services/google_gemini_service.py

import google.generativeai as genai
from pathlib import Path
import os
import json
from src.schemas.product_schema_simplified import product_schema
from google.protobuf.json_format import MessageToDict

# from src.utils.schema_utils import get_product_schema_without_additional_properties  # Import utility

import typing_extensions as typing

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])


def describe_product_from_image(image_path: Path):
    """
    Uploads a product image to the Google Gemini API and retrieves structured product details
    based on the defined product schema.
    
    Args:
    - image_path: The local path to the product image file.
    
    Returns:
    - A dictionary containing the product details based on the Product schema.
    """
    try:
        # Upload the image file to Google Gemini API
        uploaded_file = genai.upload_file(image_path)
        print(f"Uploaded File: {uploaded_file}")

        # Instantiate the model and configure it to return product data in JSON format based on the Product schema
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        # prompt = "Describe the attached product and reply in this JSON format ."
        prompt = "Analyze the image and provide a detailed product description in JSON format, including the following information: \
                * **Barcode number** (if visible) \
                * **Barcode formats** (if visible) \
                * **Manufacturer part number (MPN)** \
                * **Model number** \
                * **ASIN** \
                * **Title** \
                * **Category** \
                * **Brand** \
                * **Color** \
                * **Size** \
                * **Material** (if identifiable) \
                * **Description** \
                * **Features** (as a list) \
                * **Images** (if available online) \
                \
                Please ensure the output is formatted as a valid JSON object."
        # product_schema = get_product_schema_without_additional_properties(Product)

        # Generate content using the schema-based configuration
        result = model.generate_content(
            [uploaded_file,prompt],
            generation_config=genai.GenerationConfig(
            response_mime_type="application/json"  # Use the Product schema for response validation
            )
        )
        print(f"RESULT --> {result}")
        json_text = result.candidates[0].content.parts[0].text
        # Return the structured product data as a dictionary
        
        # Parse the JSON string into a dictionary
        result_dict = json.loads(json_text)

        print(f"RESULT is {result_dict}")
        # Return the structured product data as a dictionary
        return result_dict

    except Exception as e:
        raise Exception(f"Error processing image with Google Gemini: {e}")
