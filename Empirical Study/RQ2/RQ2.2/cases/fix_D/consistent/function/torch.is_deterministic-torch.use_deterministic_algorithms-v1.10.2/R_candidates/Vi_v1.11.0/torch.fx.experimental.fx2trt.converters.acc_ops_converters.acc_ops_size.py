@tensorrt_converter(acc_ops.size)
def acc_ops_size(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"size received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if not has_dynamic_shape(input_val.shape):
        if network.has_implicit_batch_dimension:
            return torch.Size((IMPLICIT_BATCH_DIM,) + tuple(input_val.shape))
        return torch.Size(input_val.shape)

    layer = network.add_shape(input_val)
    set_layer_name(layer, target, name)
    return layer.get_output(0)
