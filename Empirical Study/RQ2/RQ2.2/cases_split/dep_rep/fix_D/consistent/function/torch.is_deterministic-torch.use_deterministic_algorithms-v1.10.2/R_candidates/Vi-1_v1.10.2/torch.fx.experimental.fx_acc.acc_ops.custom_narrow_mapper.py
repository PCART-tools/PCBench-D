@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.narrow),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim", "dim"),
        ("start", "start"),
        ("length", "length"),
    ],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "narrow"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim", "dim"),
        ("start", "start"),
        ("length", "length"),
    ],
)
def custom_narrow_mapper(node: torch.fx.Node, mod: nn.Module) -> torch.fx.Node:
    assert isinstance(node.kwargs["start"], int) and isinstance(
        node.kwargs["length"], int
    )
    kwargs = {
        "input": node.kwargs["input"],
        "dims": (node.kwargs["dim"],),
        "starts": (node.kwargs["start"],),
        "stops": (node.kwargs["start"] + node.kwargs["length"],),
        "steps": (1,),
    }
    with node.graph.inserting_before(node):
        new_node = node.graph.call_function(slice_tensor, kwargs=kwargs)
    new_node.meta = node.meta.copy()
    return new_node
