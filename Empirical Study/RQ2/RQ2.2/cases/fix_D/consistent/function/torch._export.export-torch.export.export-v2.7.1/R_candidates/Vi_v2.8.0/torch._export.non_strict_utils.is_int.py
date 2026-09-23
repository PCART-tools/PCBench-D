def is_int(x: object) -> bool:
    return isinstance(x, int) or (isinstance(x, torch.SymInt) and x.node.expr.is_number)
