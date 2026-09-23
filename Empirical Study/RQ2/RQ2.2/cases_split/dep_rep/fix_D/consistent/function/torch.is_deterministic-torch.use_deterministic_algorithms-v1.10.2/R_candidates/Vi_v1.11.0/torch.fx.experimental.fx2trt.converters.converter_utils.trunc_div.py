def trunc_div(
    input: TRTTensor,
    other: TRTTensor,
    network: TRTNetwork,
    target: Target,
    name: str
) -> TRTTensor:
    """
    Perform trunc divide on Tensor, result of divide will be round toward zero.
    This means for positive number, it will be floor round; for negative number,
    it will be ceil round. Example: [2.1, 0.8, -3.2] -> [2, 0, -3].

    Args:
        input: divisor.
        other: dividend.
        network: INetworkDefinition.
        target: node target.
        name: namespace for the op

    Returns:
        A TensorRT tensor represent the result of trunc divide.
    """
    prod_output = add_binary_elementwise_layer(network, input, other, trt.ElementWiseOperation.PROD, target, f"{name}_prod")
    sign_output = sign(network, prod_output, target, name)

    # Convert constant input into ITensor for UnaryOperation
    if not isinstance(input, trt.tensorrt.ITensor):
        input = get_trt_tensor(network, input, f"{name}_input")
    if not isinstance(other, trt.tensorrt.ITensor):
        other = get_trt_tensor(network, other, f"{name}_other", dtype=torch_dtype_from_trt(input.dtype))

    abs_input_output = add_unary_layer(network, input, trt.UnaryOperation.ABS, target, f"{name}_abs_input")
    abs_other_output = add_unary_layer(network, other, trt.UnaryOperation.ABS, target, f"{name}_abs_other")
    abs_floor_output = add_binary_elementwise_layer(network, abs_input_output, abs_other_output,
                                                    trt.ElementWiseOperation.FLOOR_DIV, target, f"{name}_floor_div")
    output = add_binary_elementwise_layer(network, abs_floor_output, sign_output,
                                          trt.ElementWiseOperation.PROD, target, f"{name}_output")

    return output
