@tensorrt_converter(acc_ops.permute)
def acc_ops_permute(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    ranks = len(input_val.shape) + (1 if network.has_implicit_batch_dimension else 0)  # type: ignore[union-attr]
    permutation = [get_positive_dim(i, ranks) for i in cast(Sequence[int], kwargs["permutation"])]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"permute received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if network.has_implicit_batch_dimension:
        assert permutation[0] == 0, "Can't permute batch dimension when it's implicit."
        permutation = [i - 1 for i in permutation[1:]]

    layer = network.add_shuffle(input_val)
    layer.second_transpose = tuple(permutation)
    set_layer_name(layer, target, name)
    return layer.get_output(0)
