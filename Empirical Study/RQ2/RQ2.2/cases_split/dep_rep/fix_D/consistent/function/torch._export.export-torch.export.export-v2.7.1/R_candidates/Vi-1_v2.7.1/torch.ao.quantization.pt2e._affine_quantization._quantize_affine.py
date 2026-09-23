@register_custom_op
def _quantize_affine(
    input: torch.Tensor,
    block_size: list[int],
    scale: torch.Tensor,
    zero_point: Optional[torch.Tensor],
    output_dtype: torch.dtype,
    quant_min: Optional[Union[int, float, bool]] = None,
    quant_max: Optional[Union[int, float, bool]] = None,
    zero_point_domain: Optional[str] = ZeroPointDomain.INT.name,
) -> torch.Tensor:
    """op definition that has compatible signatures with custom op library

    Note:
        zero_point_domain is optional specifies how we quantize the floating point to quantized data:
        INT: quantized_val = (float_val / scale) (integer) + zero_point (integer)
        FLOAT: quantized_val = (float_val - (zero_point (float) - scale * mid_point)) / scale
        None: quantized_val = (float_val / scale) | this is primarily used for floatx quantization
            Where we do not want to round values to nearest integer and instead scale and cast.
    """
    quant_min, quant_max = _get_and_check_qmin_qmax(output_dtype, quant_min, quant_max)
    # workaround for uintx dtypes, since we don't have native Uintx dtype connected with
    # torch.uintx dtypes yet
    if output_dtype in _SUB_BYTE_UINT_BOUNDS:
        output_dtype = torch.uint8
    return _quantize_affine_no_dtype_cast(
        input,
        block_size,
        scale,
        zero_point,
        quant_min,
        quant_max,
        zero_point_domain,
    ).to(output_dtype)
