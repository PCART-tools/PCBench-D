@tensorrt_converter(torch.nn.modules.pooling.MaxPool2d)
def maxpool2d(network, submod, args, kwargs, layer_name):
    # args/kwargs should have already been normalized to kwargs
    assert len(args) == 0
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"MaxPool2d received input {input_val} that is not part "
                           "of the TensorRT region!")

    return common_maxpool(network, submod, dimension=2, input_val=input_val, layer_name=layer_name)
