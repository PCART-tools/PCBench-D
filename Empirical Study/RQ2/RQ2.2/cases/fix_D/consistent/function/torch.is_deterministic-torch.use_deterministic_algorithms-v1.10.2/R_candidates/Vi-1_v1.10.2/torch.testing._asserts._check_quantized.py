def _check_quantized(
    check_tensor_values: Callable[..., Optional[_TestingErrorMeta]]
) -> Callable[..., Optional[_TestingErrorMeta]]:
    """Decorates non-quantized tensor check functions to handle quantized tensors.

    If the inputs are not quantized, this decorator is a no-op.

    Args:
        check_tensor_values (Callable[..., Optional[_TestingErrorMeta]]): Tensor check function for continuous tensors.

    Returns:
        Optional[_TestingErrorMeta]: Return value of :attr:`check_tensors`.
    """

    @functools.wraps(check_tensor_values)
    def wrapper(actual: Tensor, expected: Tensor, **kwargs: Any) -> Optional[_TestingErrorMeta]:
        if not actual.is_quantized:
            return check_tensor_values(actual, expected, **kwargs)

        return check_tensor_values(actual.dequantize(), expected.dequantize(), **kwargs)

    return wrapper
