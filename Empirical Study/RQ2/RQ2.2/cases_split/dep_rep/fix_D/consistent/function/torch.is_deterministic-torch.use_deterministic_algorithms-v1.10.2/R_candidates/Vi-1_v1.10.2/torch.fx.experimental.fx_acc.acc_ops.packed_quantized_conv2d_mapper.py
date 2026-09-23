@register_custom_acc_mapper_fn(
    op_and_target=("call_module", nn.quantized.Conv2d),
    arg_replacement_tuples=[
        ("input", "input"),
    ],
)
def packed_quantized_conv2d_mapper(
    node: torch.fx.Node, mod: nn.Module
) -> torch.fx.Node:
    """
    Mapping from quantzed Conv2d module to acc_op.conv. We unpack all the parameters
    in this mapper and pass them directly to conv2d node.
    """
    assert isinstance(node.target, str)
    conv_module = dict(mod.named_modules())[node.target]
    prefix = node.target.replace(".", "_")
    weight_name = f"{prefix}_weight"
    bias_name = f"{prefix}_bias"

    # Store weight and bias in the main module
    mod.register_buffer(weight_name, conv_module.weight())
    if conv_module.bias() is not None:
        mod.register_buffer(bias_name, conv_module.bias())

    with node.graph.inserting_before(node):
        # Insert get_attr nodes for weight and bias
        get_weight = node.graph.get_attr(weight_name)
        get_weight.meta["tensor_meta"] = _extract_tensor_metadata(conv_module.weight())

        get_bias = None
        if conv_module.bias() is not None:
            get_bias = node.graph.get_attr(bias_name)
            get_bias.meta["tensor_meta"] = _extract_tensor_metadata(conv_module.bias())

        # Create kwargs for acc_op.conv
        kwargs = {
            "input": node.kwargs["input"],
            "weight": get_weight,
            "bias": get_bias,
            "stride": conv_module.stride,
            "padding": conv_module.padding,
            "dilation": conv_module.dilation,
            "groups": conv_module.groups,
            "padding_mode": conv_module.padding_mode,
            "acc_out_ty": acc_utils.build_raw_tensor_meta(
                q_scale=conv_module.scale, q_zero_point=conv_module.zero_point
            ),
        }

        new_node = node.graph.call_function(quantized_conv2d, kwargs=kwargs)
        new_node.meta = node.meta
        return new_node
