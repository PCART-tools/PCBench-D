def get_quantized_operator(float_op: Union[Callable, str]) -> Callable:
    """Get the quantized operator corresponding to the float operator"""
    quantized_op = DEFAULT_FLOAT_TO_QUANTIZED_OPERATOR_MAPPINGS.get(float_op, None)
    assert (
        quantized_op is not None
    ), f"Operator {str(float_op)} does not have corresponding quantized op"
    return quantized_op
