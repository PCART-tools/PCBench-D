def _is_connected(source: torch.fx.Node, dest: torch.fx.Node) -> bool:
    """
    Assuming dest is one of the ops inserted by quant workflow, this function
    finds if source and dest are connected. Assumption is that only quant workflow
    inserted ops exist between source and dest
    """
    quant_workflow_ops = _QUANTIZE_OPS + _DEQUANTIZE_OPS
    quant_workflow_ops.append(torch.ops.quantized_decomposed.choose_qparams.tensor)
    while dest.target in quant_workflow_ops:
        if not isinstance(dest.args[0], torch.fx.Node):
            raise ValueError(
                f"expected arg[0] of quant workflow ops to be a node but found {dest.args[0]}"
            )
        dest = dest.args[0]
    return dest == source
