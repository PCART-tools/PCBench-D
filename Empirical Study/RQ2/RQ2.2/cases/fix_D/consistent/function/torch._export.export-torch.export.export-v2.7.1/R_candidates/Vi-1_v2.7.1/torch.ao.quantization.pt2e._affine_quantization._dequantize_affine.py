@register_custom_op
def _dequantize_affine(
    input: torch.Tensor,
    block_size: list[int],
    scale: torch.Tensor,
    zero_point: Optional[torch.Tensor],
    input_dtype: torch.dtype,
    quant_min: Optional[Union[int, float, bool]] = None,
    quant_max: Optional[Union[int, float, bool]] = None,
    zero_point_domain: Optional[str] = ZeroPointDomain.INT.name,
    output_dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """op definition that has compatible signatures with custom op library"""
    # TODO: validate scale/zero_point dimensions are compatible with block_size
    if input_dtype not in _SUB_BYTE_UINT_BOUNDS:
        assert (
            input.dtype == input_dtype
        ), f"Expected: {input_dtype}, got: {input.dtype}"
    assert output_dtype in [
        torch.float32,
        torch.float16,
        torch.bfloat16,
    ], f"Unsupported output dtype: {output_dtype}"
    quant_min, quant_max = _get_and_check_qmin_qmax(input_dtype, quant_min, quant_max)
    return _dequantize_affine_no_dtype_check(
        input,
        block_size,
        scale,
        zero_point,
        quant_min,
        quant_max,
        zero_point_domain,
        output_dtype,
    )
