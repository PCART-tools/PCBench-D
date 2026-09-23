@tensorrt_converter(acc_ops.softmax)
def acc_ops_softmax(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    dim = kwargs["dim"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"softmax received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    # Used to get dim when dim is None. Copied from PyTorch softmax implementation.
    def get_softmax_dim(ndim):
        if ndim == 0 or ndim == 1 or ndim == 3:
            ret = 0
        else:
            ret = 1
        return ret

    if dim is None:
        dim = get_softmax_dim(
            len(input_val.shape)
            if not network.has_implicit_batch_dimension
            else len(input_val.shape) + 1
        )

    if network.has_implicit_batch_dimension:
        assert dim != 0, "Can't apply softmax on batch dimension when it's implicit."
        dim = (dim % (len(input_val.shape) + 1)) - 1

    layer = network.add_softmax(input_val)
    layer.axes = 1 << dim
    layer.name = name
    return layer.get_output(0)
