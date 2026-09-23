@tensorrt_converter(torch.nn.modules.linear.Linear)
def linear(network, submod, args, kwargs, layer_name):
    # args/kwargs should have already been normalized to kwargs
    assert len(args) == 0
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"Linear received input {input_val} that is not part "
                           "of the TensorRT region!")

    return common_linear(network, submod, input_val, layer_name, is_quantized=False)
