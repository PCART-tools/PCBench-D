def reduce_op_mapper(
    node: torch.fx.Node, mod: torch.fx.GraphModule, func
) -> torch.fx.Node:
    with node.graph.inserting_before(node):
        kwargs = dict(node.kwargs)
        if "dim" in kwargs and isinstance(kwargs["dim"], int):
            kwargs["dim"] = (kwargs["dim"],)
        new_node = node.graph.call_function(func, kwargs=kwargs)
        new_node.meta = node.meta.copy()
        return new_node
