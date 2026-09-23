@tensorrt_converter(torch.mul)
@tensorrt_converter(operator.mul)
def mul(network, target, args, kwargs, layer_name):
    # operator.mul
    if len(kwargs) == 0:
        lhs_val, rhs_val = args
    else:
        # torch.mul
        lhs_val, rhs_val = kwargs["input"], kwargs["other"]

    if not all(isinstance(arg, trt.tensorrt.ITensor) for arg in [lhs_val, rhs_val]):
        raise RuntimeError('mul() received an input that is not part of the TensorRT region!')

    layer = network.add_elementwise(lhs_val, rhs_val, trt.ElementWiseOperation.PROD)
    layer.name = layer_name

    return layer.get_output(0)
