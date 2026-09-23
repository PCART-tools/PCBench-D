@tensorrt_converter(acc_ops.softsign)
def acc_ops_softsign(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    operation_type = trt.ActivationType.SOFTSIGN
    return add_activation_layer(network, input_val, operation_type, target, name)
