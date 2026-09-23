@tensorrt_converter(acc_ops.softmax)
def acc_ops_softmax(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    input_ranks = len(input_val.shape) + (1 if network.has_implicit_batch_dimension else 0)  # type: ignore[union-attr]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"softmax received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    # Used to get dim when dim is None. Copied from PyTorch softmax implementation.
    def get_softmax_dim(ndim: int) -> int:
        if ndim == 0 or ndim == 1 or ndim == 3:
            ret = 0
        else:
            ret = 1
        return ret

    if kwargs["dim"] is None:
        dim = get_softmax_dim(input_ranks)
    else:
        dim = cast(int, kwargs["dim"])

    dim = get_positive_dim(dim, input_ranks)
    if network.has_implicit_batch_dimension:
        assert dim != 0, "Can't apply softmax on batch dimension when it's implicit."
        dim -= 1

    layer = network.add_softmax(input_val)
    layer.axes = 1 << dim
    set_layer_name(layer, target, name)
    return layer.get_output(0)
