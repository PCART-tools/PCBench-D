@tensorrt_converter(torch.nn.quantized.modules.batchnorm.BatchNorm2d)
def quantized_batchnorm2d(network, submod, args, kwargs, layer_name):
    input_val = args[0]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f'Quantized BatchNorm2d received input {input_val} that is not part '
                           'of the TensorRT region!')

    return common_batchnorm(network, submod, input_val, layer_name, is_quantized=True)
