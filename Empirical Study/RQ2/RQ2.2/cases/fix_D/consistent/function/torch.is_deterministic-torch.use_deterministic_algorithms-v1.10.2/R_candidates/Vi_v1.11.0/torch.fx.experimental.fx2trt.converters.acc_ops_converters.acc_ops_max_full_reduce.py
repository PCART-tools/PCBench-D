@tensorrt_converter(acc_ops.max_full_reduce, no_implicit_batch_dim=True)
def acc_ops_max_full_reduce(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    return add_acc_ops_full_reduce(network, target, args, kwargs, name, trt.ReduceOperation.MAX)
