@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.dequantize),
    arg_replacement_tuples=[("input", "input")],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "dequantize"),
    arg_replacement_tuples=[("input", "input")],
)
def custom_dequantize_mapper(node: torch.fx.Node, mod: nn.Module) -> torch.fx.Node:
    assert isinstance(node.kwargs["input"], torch.fx.Node)
    assert "tensor_meta" in node.kwargs["input"].meta
    new_kwargs = {
        "input": node.kwargs["input"],
        "input_tensor_meta": node.kwargs["input"].meta["tensor_meta"],
    }
    # `input_tensor_meta` contains quantization parameters that can be used to lower
    # acc_ops.dequantize to TensorRT ops
    with node.graph.inserting_before(node):
        new_node = node.graph.create_node(
            "call_function", dequantize, kwargs=new_kwargs, name=node.name
        )
        assert isinstance(node, torch.fx.Node)
        new_node.meta = node.meta
        return new_node
