@tensorrt_converter("dequantize")
@tensorrt_converter(torch.dequantize)
@tensorrt_converter(torch.nn.quantized.modules.DeQuantize)
def dequantize(network, submod, args, kwargs, layer_name):
    input_val = args[0]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f'Dequantize received input {input_val} that is not part '
                           'of the TensorRT region!')

    return input_val
