@tensorrt_converter(acc_ops.mean)
def acc_ops_mean(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> TRTTensor:
    return add_reduce_layer(network, target, args, kwargs, trt.ReduceOperation.AVG, name)
