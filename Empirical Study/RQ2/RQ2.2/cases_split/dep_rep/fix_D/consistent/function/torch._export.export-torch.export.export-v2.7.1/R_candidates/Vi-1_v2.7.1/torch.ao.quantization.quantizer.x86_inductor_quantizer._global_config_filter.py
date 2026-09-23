def _global_config_filter(nodes: list[Node]) -> bool:
    """Filter function for global configuration.

    This filter function takes a list of nodes and returns True if there is exactly one node
    in the list that is a default quantizable operation, False otherwise.
    """
    num_nodes_in_default_quantizable_ops = sum(
        node.target in default_quantizable_ops for node in nodes
    )
    if num_nodes_in_default_quantizable_ops > 1:
        raise NotImplementedError(
            "Several nodes within a single pattern are default quantizable operations."
        )
    return num_nodes_in_default_quantizable_ops == 1
