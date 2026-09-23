def _is_int(expr: object) -> bool:
    return isinstance(expr, SymInt) and expr.node.expr.is_number
