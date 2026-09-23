@register_custom_acc_mapper_fn(
    op_and_target=("call_module", nn.quantized.Linear),
    arg_replacement_tuples=[
        ("input", "input"),
    ],
)
def packed_quantized_linear_mapper(
    node: torch.fx.Node, mod: nn.Module
) -> torch.fx.Node:
    """
    Mapping from quantized_linear module to acc_op.linear. We unpack weight and bias
    in this mapper and pass them directly to linear node.
    """
    assert isinstance(node.target, str)
    linear_module = dict(mod.named_modules())[node.target]
    prefix = node.target.replace(".", "_")
    weight_name = f"{prefix}_weight"
    bias_name = f"{prefix}_bias"

    # Store weight and bias in the main module
    mod.register_buffer(weight_name, linear_module.weight())
    if linear_module.bias() is not None:
        mod.register_buffer(bias_name, linear_module.bias())

    with node.graph.inserting_before(node):
        # Insert get_attr nodes for weight and bias
        get_weight = node.graph.get_attr(weight_name)
        get_weight.meta["tensor_meta"] = _extract_tensor_metadata(
            linear_module.weight()
        )

        get_bias = None
        if linear_module.bias() is not None:
            get_bias = node.graph.get_attr(bias_name)
            get_bias.meta["tensor_meta"] = _extract_tensor_metadata(
                linear_module.bias()
            )

        qparams = {"scale": linear_module.scale, "zero_point": linear_module.zero_point}
        # Create kwargs for acc_op.quantized_linear
        kwargs = {
            "input": node.kwargs["input"],
            "weight": get_weight,
            "bias": get_bias,
            "acc_out_ty": acc_utils.build_raw_tensor_meta(qparams=qparams),
        }

        new_node = node.graph.call_function(quantized_linear, kwargs=kwargs)
        new_node.meta = node.meta
        return new_node
