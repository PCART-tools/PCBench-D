@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "to"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dtype", "dtype"),
    ],
)
def custom_tensor_to_mapper(node: torch.fx.Node, _: nn.Module):
    dest_dtype = node.kwargs["dtype"]
    mem_format = node.kwargs.get("memory_format")
    device = node.kwargs.get("device")
    assert dest_dtype is not None
    assert mem_format is None or mem_format == torch.preserve_format
    assert device is None

    new_kwargs = {
        "input": node.kwargs["input"],
        "acc_out_ty": acc_utils.build_raw_tensor_meta(dtype=dest_dtype),
    }

    with node.graph.inserting_before(node):
        new_node = node.graph.create_node(
            "call_function", to_dtype, kwargs=new_kwargs, name=node.name
        )
        new_node.meta = node.meta
        return new_node
