@tensorrt_converter(acc_ops.max_dim_reduce)
def acc_ops_max_dim_reduce(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    return add_acc_ops_dim_reduce(network, target, args, kwargs, name, trt.ReduceOperation.MAX)
