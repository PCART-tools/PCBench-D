def _dtype_getter_instructions(name: str, args: Tuple[Any, ...], kwargs: Dict[str, Any], return_value: Any) -> str:
    return f"This call to {name}(...) can be replaced with {return_value}."
