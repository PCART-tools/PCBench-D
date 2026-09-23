def is_pydantic_model(value: Any) -> bool:
    """Check whether value derives from a pydantic.BaseModel."""
    return _check_for_pydantic(value) and isinstance(value, pydantic.BaseModel)
