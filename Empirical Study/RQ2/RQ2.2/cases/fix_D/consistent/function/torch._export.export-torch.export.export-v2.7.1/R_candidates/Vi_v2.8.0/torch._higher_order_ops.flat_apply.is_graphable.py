def is_graphable(val) -> bool:
    """Definition: a graphable type is a type that that is an acceptable input/output type to a FX node."""
    return isinstance(val, torch.fx.node.base_types)
