@tensorrt_converter(torch.nn.quantized.modules.linear.Linear)
def quantized_linear(network, submod, args, kwargs, layer_name):
    input_val = args[0]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"Quantized Linear received input {input_val} that is not part "
                           "of the TensorRT region!")

    return common_linear(network, submod, input_val, layer_name, is_quantized=True)
