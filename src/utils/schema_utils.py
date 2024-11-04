# src/utils/schema_utils.py

from pydantic import BaseModel
import copy

def remove_additional_properties(schema: dict) -> dict:
    """
    Recursively removes 'additionalProperties' from a Pydantic schema.
    """
    if isinstance(schema, dict):
        schema = copy.deepcopy(schema)  # Create a deep copy of the schema
        schema.pop('additionalProperties', None)  # Remove additionalProperties if present
        for key, value in schema.items():
            if isinstance(value, dict):
                schema[key] = remove_additional_properties(value)
            elif isinstance(value, list):
                schema[key] = [remove_additional_properties(v) for v in value]
    return schema

def get_product_schema_without_additional_properties(model: BaseModel) -> dict:
    """
    Returns the Pydantic schema for a given model without 'additionalProperties'.
    """
    schema = model.schema()  # Generate the Pydantic schema
    return remove_additional_properties(schema)
