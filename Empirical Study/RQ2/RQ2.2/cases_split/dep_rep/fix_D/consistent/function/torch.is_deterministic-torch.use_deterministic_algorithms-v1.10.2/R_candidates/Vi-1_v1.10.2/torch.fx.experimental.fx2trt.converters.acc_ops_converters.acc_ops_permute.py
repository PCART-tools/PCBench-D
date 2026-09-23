@tensorrt_converter(acc_ops.permute)
def acc_ops_permute(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    permutation = kwargs["permutation"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"permute received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    if network.has_implicit_batch_dimension:
        assert permutation[0] == 0, "Can't permute batch dimension when it's implicit."
        permutation = [i - 1 for i in permutation[1:]]

    layer = network.add_shuffle(input_val)
    layer.second_transpose = tuple(permutation)
    layer.name = name
    return layer.get_output(0)
