@register_custom_acc_mapper_fn(
    op_and_target=("call_module", nn.intrinsic.quantized.ConvReLU2d),
    arg_replacement_tuples=[
        ("input", "input"),
    ],
)
def packed_quantized_convrelu2d_mapper(
    node: torch.fx.Node, mod: nn.Module
) -> torch.fx.Node:
    """
    Mapping from quantized ConvReLU2d module to acc_op.relu. We use packed_quantized_conv2d_mapper to unpack all the parameters
    in this mapper and pass the returned conv2d node directly to relu node.
    """

    with node.graph.inserting_before(node):
        # conv2d op
        conv2d_node = packed_quantized_conv2d_mapper(node, mod)

        # relu op
        relu_node = node.graph.call_function(
            relu, kwargs={"input": conv2d_node, "inplace": False}
        )
        relu_node.meta = node.meta
        return relu_node
