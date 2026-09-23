@register_custom_acc_mapper_fn(
    op_and_target=("call_function", torch.ops.quantized.add_relu),
    arg_replacement_tuples=[
        ("input", "input"),
        ("other", "other"),
        ("scale", "scale"),
        ("zero_point", "zero_point"),
    ],
)
def add_relu_unfuse_mapper(
    node: torch.fx.Node, mod: torch.fx.GraphModule
) -> torch.fx.Node:
    with node.graph.inserting_before(node):
        qparams = {
            "scale": node.kwargs["scale"],
            "zero_point": node.kwargs["zero_point"],
        }
        add_kwargs = {
            "input": node.kwargs["input"],
            "other": node.kwargs["other"],
            "acc_out_ty": acc_utils.build_raw_tensor_meta(qparams=qparams),
        }
        add_node = node.graph.call_function(quantized_add, kwargs=add_kwargs)
        add_node.meta = node.meta.copy()

        relu_node = node.graph.call_function(
            relu, kwargs={"input": add_node, "inplace": False}
        )
        relu_node.meta = node.meta
        return relu_node
