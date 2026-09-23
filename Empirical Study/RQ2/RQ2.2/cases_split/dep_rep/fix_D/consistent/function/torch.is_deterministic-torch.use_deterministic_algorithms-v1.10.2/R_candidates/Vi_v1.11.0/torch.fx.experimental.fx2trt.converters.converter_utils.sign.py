def sign(
    network: TRTNetwork,
    input_val: TRTTensor,
    target: Target,
    name: str
) -> TRTTensor:
    """
    Sign is calculated as below:
       x = input
       sign = (exp(x) // exp(abs(x))) * 2 - 1
       For positive number and 0, (exp(x) // exp(abs(x))) yield 1; for negative number, (exp(x) // exp(abs(x))) yield 0.
       With multiply 2, the value become 2(for pos and 0) and 0(for neg).
       Finally minus 1, the value become 1(for pos and 0) and -1(for neg).

    Args:
        network (TRTNetwork): TensorRT network object.
        input_val (TRTTensor): The input tensor.
        target (Target): fx node target.
        name (str): Name of the fx node with optional suffix.

    Returns:
        A TensorRT tensor represent the result of sign operator.
    """
    input_exp_output = add_unary_layer(network, input_val, trt.UnaryOperation.EXP, target, f"{name}_prod_exp")
    input_abs_output = add_unary_layer(network, input_val, trt.UnaryOperation.ABS, target, f"{name}_prod_abs")
    input_abs_exp_output = add_unary_layer(network, input_abs_output, trt.UnaryOperation.EXP, target, f"{name}_prod_abs_exp")
    floor_div_output = add_binary_elementwise_layer(network, input_exp_output, input_abs_exp_output,
                                                    trt.ElementWiseOperation.FLOOR_DIV, target, f"{name}_exp_floor_div")
    double_floor_div_output = add_binary_elementwise_layer(network, floor_div_output, 2,
                                                           trt.ElementWiseOperation.PROD, target, f"{name}_floor_div*2")
    return add_binary_elementwise_layer(network, double_floor_div_output, 1,
                                        trt.ElementWiseOperation.SUB, target, f"{name}_sign")
