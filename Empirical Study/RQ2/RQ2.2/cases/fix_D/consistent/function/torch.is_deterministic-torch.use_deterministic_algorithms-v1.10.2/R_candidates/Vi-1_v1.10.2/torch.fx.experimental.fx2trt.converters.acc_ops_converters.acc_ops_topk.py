@tensorrt_converter(acc_ops.topk)
def acc_ops_topk(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"topk received input {input_val} that is not part "
                           "of the TensorRT region!")

    if kwargs["sorted"] and kwargs["k"] != 1:
        raise RuntimeError("Currently we don't support sorted=True in topk.")

    if not network.has_implicit_batch_dimension and len(input_val.shape) <= 1:
        raise RuntimeError("At least 2 dimensions are required for input to topk.")

    num_dims = len(input_val.shape) + (1 if network.has_implicit_batch_dimension else 0)
    k = kwargs["k"]
    dim = (kwargs["dim"] if kwargs["dim"] is not None else -1) % num_dims
    operation = trt.TopKOperation.MAX if kwargs["largest"] else trt.TopKOperation.MIN
    layer = network.add_topk(
        input_val, operation, k, get_axes_for_reduce_op(dim, network.has_implicit_batch_dimension)
    )
    layer.name = name
    return layer.get_output(0), layer.get_output(1)
