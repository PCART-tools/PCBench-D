def _to_ast(expr: str) -> ast.expr:
    """
    Converts a Python string to an AST.

    This will take the Python Arrow expression (as a string), and it will
    be converted into a Python AST that can be traversed to convert it to a PyIceberg
    expression.

    The reason to convert it to an AST is because the PyArrow expression
    itself doesn't have any methods/properties to traverse the expression.
    We need this to convert it into a PyIceberg expression.

    Parameters
    ----------
    expr
        The string expression

    Returns
    -------
    The AST representing the Arrow expression
    """
    return ast.parse(expr, mode="eval").body
