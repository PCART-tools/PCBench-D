def is_graphable_type(typ) -> bool:
    """Return whether the given type is graphable"""
    return issubclass(typ, torch.fx.node.base_types)
