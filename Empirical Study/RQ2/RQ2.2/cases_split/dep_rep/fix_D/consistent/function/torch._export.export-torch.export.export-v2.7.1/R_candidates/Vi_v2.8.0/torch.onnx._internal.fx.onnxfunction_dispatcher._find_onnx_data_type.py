def _find_onnx_data_type(
    torch_input: fx_type_utils.TensorLike
    | str
    | int
    | float
    | bool
    | list
    | tuple
    | complex
    | None,
) -> set[str]:
    """Convert inputs data type from torch acceptable dtype to the compatible onnx dtype string."""
    if (
        isinstance(torch_input, fx_type_utils.TensorLike)
        and torch_input.dtype is not None
    ):
        return fx_type_utils.from_torch_dtype_to_onnx_dtype_str(torch_input.dtype)
    if isinstance(torch_input, (int, float, bool, str, complex)):
        return fx_type_utils.from_torch_dtype_to_onnx_dtype_str(type(torch_input))
    if isinstance(torch_input, (list, tuple)) and torch_input:  # [Tensor, Tensor]
        the_first_non_none_item = next(
            (item for item in torch_input if item is not None), None
        )
        set_dtype = _find_onnx_data_type(the_first_non_none_item)
        if any(isinstance(input, fx_type_utils.TensorLike) for input in torch_input):
            # NOTE: Any Tensor involved in a list would make it a seq(tensor(onnx_type))
            return {f"seq({dtype})" for dtype in set_dtype}
        else:
            # constant list of non-tensor type
            return set_dtype
    if (
        torch_input is None
        or (
            isinstance(torch_input, fx_type_utils.TensorLike)
            and torch_input.dtype is None
        )
        or (isinstance(torch_input, (list, tuple)) and not torch_input)
    ):
        # NOTE: None, No dtype, and empty list are edge cases, we allow it to be any type to relax the type check
        # seq(tensor) also goes to here, as it is not supported in torchscript, and it would be None in this case.
        return set()

    raise RuntimeError(f"Unknown input type from input: {torch_input}")
