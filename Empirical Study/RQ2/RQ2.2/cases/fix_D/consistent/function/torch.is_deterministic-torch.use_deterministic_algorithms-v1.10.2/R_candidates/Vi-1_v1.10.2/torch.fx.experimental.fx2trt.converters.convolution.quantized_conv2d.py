@tensorrt_converter(torch.nn.quantized.modules.conv.Conv2d)
def quantized_conv2d(network, submod, args, kwargs, layer_name):
    input_val = args[0]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f'Quantized Conv2d received input {input_val} that is not part '
                           'of the TensorRT region!')

    return common_conv(network, submod, dimension=2, input_val=input_val, layer_name=layer_name, is_quantized=True)
