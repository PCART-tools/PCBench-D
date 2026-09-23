@tensorrt_converter(torch.nn.intrinsic.quantized.modules.ConvReLU2d)
def quantized_conv_relu2d(network, submod, args, kwargs, layer_name):
    input_val = args[0]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f'Quantized ConvReLU2d received input {input_val} that is not part '
                           'of the TensorRT region!')

    return common_conv_relu(network, submod, dimension=2, input_val=input_val, layer_name=f"{layer_name}_conv", is_quantized=True)
