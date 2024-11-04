# src/schemas/product_schema.py

product_schema = {
    "type": "object",
    "properties": {
        "product_details": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "vendor": {"type": "string"},
                "product_type": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "sku": {"type": "string"},
                "barcode": {"type": ["string", "null"]},
                "price": {"type": "number"},
                "compare_at_price": {"type": ["number", "null"]},
                "inventory_quantity": {"type": "integer"},
                "inventory_policy": {"type": "string", "enum": ["deny", "continue"]}
            },
            "required": ["title", "vendor", "price"]
        },
        "product_specifications": {
            "type": "object",
            "properties": {
                "material": {"type": "string"},
                "color": {"type": "string"},
                "size": {"type": ["string", "null"]},
                "variants": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "option": {"type": "string"},
                            "value": {"type": "string"}
                        },
                        "required": ["option", "value"]
                    }
                }
            },
            "required": ["material", "color"]
        },
        "weight": {
            "type": "object",
            "properties": {
                "value": {"type": "number"},
                "unit": {"type": "string", "enum": ["g", "kg", "oz", "lb"]}
            },
            "required": ["value", "unit"]
        },
        "dimensions": {
            "type": "object",
            "properties": {
                "length": {"type": "number"},
                "width": {"type": "number"},
                "height": {"type": "number"},
                "unit": {"type": "string", "enum": ["cm", "m", "in", "ft"]}
            },
            "required": ["length", "width", "height", "unit"]
        },
        "images": {
            "type": "array",
            "items": {"type": "string", "format": "uri"}
        }
    },
    "required": ["product_details", "product_specifications", "weight", "dimensions"]
}
