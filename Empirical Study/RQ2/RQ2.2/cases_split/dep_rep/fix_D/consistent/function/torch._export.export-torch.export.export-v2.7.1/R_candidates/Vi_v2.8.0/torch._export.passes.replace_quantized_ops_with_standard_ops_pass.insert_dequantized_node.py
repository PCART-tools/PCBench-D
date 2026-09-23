def insert_dequantized_node(
    gm: torch.fx.GraphModule,
    val_node: torch.fx.Node,
    scale_node: Union[float, torch.fx.Node],
    zero_point_node: Union[float, torch.fx.Node],
    qmin_node: Union[float, int, torch.fx.Node],
    qmax_node: Union[float, int, torch.fx.Node],
    dtype_node: Union[torch.dtype, torch.fx.Node],
    axis_node: Optional[Union[int, torch.fx.Node]],
    qscheme: Optional[torch.qscheme],
) -> torch.fx.Node:
    if qscheme is torch.per_tensor_affine:
        return gm.graph.call_function(
            dequantize_per_tensor,
            (
                val_node,
                scale_node,
                zero_point_node,
                qmin_node,
                qmax_node,
                dtype_node,
            ),
        )
    elif qscheme is torch.per_channel_affine:
        return gm.graph.call_function(
            dequantize_per_channel,
            (
                val_node,
                scale_node,
                zero_point_node,
                axis_node,
                qmin_node,
                qmax_node,
                dtype_node,
            ),
        )
    else:
        raise RuntimeError(f"Unsupported dequantization scheme: {qscheme}")
