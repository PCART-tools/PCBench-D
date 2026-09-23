@tensorrt_converter(acc_ops.sum)
def acc_ops_sum(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> TRTTensor:
    return add_reduce_layer(network, target, args, kwargs, trt.ReduceOperation.SUM, name)
