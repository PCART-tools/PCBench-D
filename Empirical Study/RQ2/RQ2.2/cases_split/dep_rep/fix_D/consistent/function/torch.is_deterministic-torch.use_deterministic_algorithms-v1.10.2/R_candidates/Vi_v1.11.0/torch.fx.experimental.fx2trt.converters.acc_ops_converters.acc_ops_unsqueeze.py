@tensorrt_converter(acc_ops.unsqueeze)
def acc_ops_unsqueeze(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"unsqueeze received input {input_val} that is not part "
                           "of the TensorRT region!")

    dim = cast(int, kwargs["dim"])
    input_shape = input_val.shape
    input_shape_size = len(input_val.shape) + 1 if network.has_implicit_batch_dimension else len(input_val.shape)
    dim = get_positive_dim(dim, input_shape_size + 1)

    if network.has_implicit_batch_dimension:
        assert dim != 0
        dim -= 1

    assert len(get_dynamic_dims(input_val.shape)) <= 1, "Currently we don't support unsqueeze with more than one dynamic dims."
    layer = network.add_shuffle(input_val)
    layer.reshape_dims = tuple(input_val.shape)[:dim] + (1,) + tuple(input_val.shape)[dim:]
    set_layer_name(layer, target, name)
    return layer.get_output(0)
