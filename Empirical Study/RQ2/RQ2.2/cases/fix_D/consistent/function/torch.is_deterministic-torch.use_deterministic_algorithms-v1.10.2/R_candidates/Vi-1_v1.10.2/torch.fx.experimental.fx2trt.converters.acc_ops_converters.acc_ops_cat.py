@tensorrt_converter(acc_ops.cat)
def acc_ops_cat(network, target, args, kwargs, name):
    tensors = kwargs["tensors"]

    if any(not isinstance(t, trt.tensorrt.ITensor) for t in tensors):
        raise RuntimeError(
            f"cat received inputs {tensors} that is not part " "of the TensorRT region!"
        )

    layer = network.add_concatenation(inputs=tensors)
    layer.axis = kwargs["dim"] - (1 if network.has_implicit_batch_dimension else 0)
    layer.name = name
    return layer.get_output(0)
