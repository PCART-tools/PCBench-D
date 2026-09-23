def field(name: str | list[str]) -> Expr:
    """
    Select a field in the current `struct.with_fields` scope.

    name
        Name of the field(s) to select.
    """
    if isinstance(name, str):
        name = [name]
    return wrap_expr(plr.field(name))
