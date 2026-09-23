def _has_uses_by_nodes(value: torch.Value, nodes: Collection[torch.Node]) -> bool:
    return any(use.user in nodes for use in value.uses())
