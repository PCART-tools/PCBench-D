@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "split"),
    arg_replacement_tuples=[
        ("tensor", "input"),
        ("split_size_or_sections", "split_size_or_sections"),
        ("dim", "dim"),
    ],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.split),
    arg_replacement_tuples=[
        ("tensor", "input"),
        ("split_size_or_sections", "split_size_or_sections"),
        ("dim", "dim"),
    ],
)
def torch_split_mapper(node: torch.fx.Node, mod: nn.Module) -> torch.fx.Node:
    """
    If split_size_or_sections is sections, map the node to slice_tensors
    + tuple_construct. Otherwise, if split_size_or_sections is split_size,
    map the node to acc_ops.split.
    """
    split_size_or_sections = node.kwargs["split_size_or_sections"]
    with node.graph.inserting_before(node):
        if isinstance(split_size_or_sections, int):
            new_kwargs = {
                "input": node.kwargs["input"],
                "split_size": split_size_or_sections,
                "dim": node.kwargs["dim"],
            }
            new_node = node.graph.call_function(split, kwargs=new_kwargs)
            new_node.meta = node.meta.copy()
            return new_node

        assert isinstance(split_size_or_sections, Sequence)
        start = 0
        slice_nodes = []
        for i in split_size_or_sections:
            assert isinstance(i, int)
            new_kwargs = {
                "input": node.kwargs["input"],
                "dims": (node.kwargs["dim"],),
                "starts": (start,),
                "stops": (start + i,),
                "steps": (1,),
            }
            new_node = node.graph.call_function(slice_tensor, kwargs=new_kwargs)
            new_node.meta["type"] = torch.Tensor
            slice_nodes.append(new_node)
            start += i

        new_node = node.graph.call_function(
            tuple_construct, kwargs={"tensors": tuple(slice_nodes)}
        )
        new_node.meta = node.meta.copy()
        return new_node
