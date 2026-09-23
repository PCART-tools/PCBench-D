@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.log1p),
    arg_replacement_tuples=[
        ("input", "input"),
    ],
)
def torch_log1p_mapper(node: torch.fx.Node, _: torch.nn.Module) -> torch.fx.Node:
    with node.graph.inserting_before(node):
        add_kwargs = {"input": node.kwargs["input"], "other": 1.0}
        add_node = node.graph.call_function(add, kwargs=add_kwargs)
        add_node.meta = node.meta.copy()
        log_kwargs = {"input": add_node}
        log_node = node.graph.call_function(log, kwargs=log_kwargs)
        log_node.meta = node.meta.copy()
        return log_node
