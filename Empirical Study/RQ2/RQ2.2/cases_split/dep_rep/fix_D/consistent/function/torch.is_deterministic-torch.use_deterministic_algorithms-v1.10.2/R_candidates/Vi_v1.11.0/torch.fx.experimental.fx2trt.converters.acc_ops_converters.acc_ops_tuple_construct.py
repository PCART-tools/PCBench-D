@tensorrt_converter(acc_ops.tuple_construct)
def acc_ops_tuple_construct(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    return kwargs["tensors"]
