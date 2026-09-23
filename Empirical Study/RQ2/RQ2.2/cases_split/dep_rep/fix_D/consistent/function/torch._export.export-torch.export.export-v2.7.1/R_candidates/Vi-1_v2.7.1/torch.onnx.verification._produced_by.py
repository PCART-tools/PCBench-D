def _produced_by(value: torch.Value, nodes: Collection[torch.Node]) -> bool:
    return value.node() in nodes
