def scatter_always_uses_mutation(node: torch.fx.Node) -> bool:
    _, _, view_ops = node.args
    return any(view.target in _ALWAYS_MUTATING_SCATTER_OPS for view in view_ops)  # type: ignore[union-attr]
