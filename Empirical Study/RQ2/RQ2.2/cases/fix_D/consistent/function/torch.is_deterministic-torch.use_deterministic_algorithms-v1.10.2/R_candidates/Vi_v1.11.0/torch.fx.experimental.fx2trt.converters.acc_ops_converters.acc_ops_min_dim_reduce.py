@tensorrt_converter(acc_ops.min_dim_reduce)
def acc_ops_min_dim_reduce(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    return add_acc_ops_dim_reduce(network, target, args, kwargs, name, trt.ReduceOperation.MIN)
