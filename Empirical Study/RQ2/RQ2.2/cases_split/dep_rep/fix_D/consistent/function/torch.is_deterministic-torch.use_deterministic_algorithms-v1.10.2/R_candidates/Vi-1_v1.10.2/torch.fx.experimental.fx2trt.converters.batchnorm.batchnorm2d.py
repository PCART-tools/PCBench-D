@tensorrt_converter(torch.nn.modules.batchnorm.BatchNorm2d)
def batchnorm2d(network, submod, args, kwargs, layer_name):
    # args/kwargs should have already been normalized to kwargs
    assert len(args) == 0
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"BatchNorm2d received input {input_val} that is not part "
                           "of the TensorRT region!")

    return common_batchnorm(network, submod, input_val, layer_name, is_quantized=False)
