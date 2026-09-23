def schema_from_sample(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract a schema compatible with 'register_rds_schema' from data.
    """
    schema = {}
    for key, value in data.items():
        if isinstance(value, str):
            schema[key] = "string"
        elif isinstance(value, int):
            schema[key] = "int"
        elif isinstance(value, float):
            schema[key] = "float"
        else:
            raise RuntimeError(f"Unsupported value type: {key}: {value}")
    return schema
