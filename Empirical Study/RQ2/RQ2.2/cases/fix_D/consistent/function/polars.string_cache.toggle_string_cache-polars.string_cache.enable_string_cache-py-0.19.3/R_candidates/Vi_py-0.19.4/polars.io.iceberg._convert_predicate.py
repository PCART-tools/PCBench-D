@singledispatch
def _convert_predicate(a: Any) -> Any:
    """Walks the AST to  convert the  PyArrow expression to a PyIceberg expression."""
    raise ValueError(f"Unexpected symbol: {a}")
