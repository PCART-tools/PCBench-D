@tensorrt_converter(acc_ops.trunc_div)
def acc_ops_trunc_div(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    return trunc_div(kwargs["input"], kwargs["other"], network, target, name)
