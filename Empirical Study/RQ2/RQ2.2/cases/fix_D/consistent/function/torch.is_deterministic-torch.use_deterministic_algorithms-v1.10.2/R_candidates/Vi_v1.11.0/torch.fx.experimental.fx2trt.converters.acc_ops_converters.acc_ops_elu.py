@tensorrt_converter(acc_ops.elu)
def acc_ops_elu(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    alpha = kwargs["alpha"]
    operation_type = trt.ActivationType.ELU
    return add_activation_layer(network, input_val, operation_type, target, name, alpha)
