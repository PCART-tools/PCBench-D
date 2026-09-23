def _all_nodes(nodes: Collection[torch.Node]) -> set[torch.Node]:
    all_nodes = set(nodes)
    for n in nodes:
        for b in n.blocks():
            all_nodes.update(_all_nodes(list(b.nodes())))
    return all_nodes
