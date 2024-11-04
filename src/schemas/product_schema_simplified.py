# src/schemas/product_schema_simplified.py

product_schema = {
    "type": "object",
    "properties": {
        "product_details": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "price": {"type": "number"},
                "sku": {"type": "string"}
            },
            "required": ["title", "price", "sku"]
        }
    },
    "required": ["product_details"]
}
