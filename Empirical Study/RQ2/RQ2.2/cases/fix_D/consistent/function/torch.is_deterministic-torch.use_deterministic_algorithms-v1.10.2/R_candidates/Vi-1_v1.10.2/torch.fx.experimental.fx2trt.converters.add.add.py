@tensorrt_converter(operator.add)
@tensorrt_converter(torch.add)
def add(network, target, args, kwargs, layer_name):
    # operator.add
    if len(kwargs) == 0:
        lhs_val, rhs_val = args
    else:
        # torch.add
        lhs_val, rhs_val = kwargs["input"], kwargs["other"]
        assert kwargs["alpha"] == 1

    if not all(isinstance(arg, trt.tensorrt.ITensor) for arg in [lhs_val, rhs_val]):
        raise RuntimeError("add() received an input that is not part of the TensorRT region!")

    layer = network.add_elementwise(lhs_val, rhs_val, trt.ElementWiseOperation.SUM)
    layer.name = layer_name

    return layer.get_output(0)
