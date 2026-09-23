@tensorrt_converter(acc_ops.selu)
def acc_ops_selu(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    operation_type = trt.ActivationType.SELU
    return add_activation_layer(network, input_val, operation_type, target, name)
