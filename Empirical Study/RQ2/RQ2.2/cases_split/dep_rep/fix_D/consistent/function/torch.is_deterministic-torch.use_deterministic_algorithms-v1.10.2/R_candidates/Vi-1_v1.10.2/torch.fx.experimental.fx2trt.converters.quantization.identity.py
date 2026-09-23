@tensorrt_converter(torch.nn.modules.linear.Identity)
def identity(network, submod, args, kwargs, layer_name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f'Identity received input {input_val} that is not part '
                           'of the TensorRT region!')

    return input_val
