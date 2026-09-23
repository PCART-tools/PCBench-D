@tensorrt_converter(acc_ops.unsqueeze)
def acc_ops_unsqueeze(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"unsqueeze received input {input_val} that is not part "
                           "of the TensorRT region!")

    dim = kwargs["dim"]
    if network.has_implicit_batch_dimension:
        assert dim != 0
        dim -= 1

    assert len(get_dynamic_dims(input_val.shape)) <= 1, "Currently we don't support unsqueeze with more than one dynamic dims."
    layer = network.add_shuffle(input_val)
    layer.reshape_dims = tuple(input_val.shape)[:dim] + (1,) + tuple(input_val.shape)[dim:]
    layer.name = name
    return layer.get_output(0)
