def _dequantize_affine_no_dtype_check(
    input: torch.Tensor,
    block_size: list[int],
    scale: torch.Tensor,
    zero_point: Optional[torch.Tensor],
    quant_min: Union[int, float],
    quant_max: Union[int, float],
    zero_point_domain: Optional[str] = ZeroPointDomain.INT.name,
    output_dtype: torch.dtype = torch.float32,
) -> torch.Tensor:
    """This function converts AQT tensors to their high precision floating point representation

    The op does the following:
    1. figure out the dimension for reduction based on block_size, also reshape the input to align with
       the shape after reduction
    2. dequantize the input based on the quantization parameters scale and zero_point and args like zero_point_domain
    3. reshape the quantized result to origianl shape and change dtype to the output_dtype
    """
    assert len(block_size) == input.dim(), (
        f"Got input dim:{input.dim()}, block_size: {block_size}"
    )
    shape_for_reduction, reduction_dims = _get_reduction_params(
        block_size, input.size()
    )
    original_shape = input.shape
    input = input.view(shape_for_reduction)
    shape_after_reduction = shape_for_reduction
    for i in reduction_dims:
        shape_after_reduction[i] = 1
    scale = scale.view(shape_after_reduction)

    if zero_point is not None:
        zero_point = zero_point.view(shape_after_reduction)

    if zero_point_domain == ZeroPointDomain.INT.name:
        # Force a copy to avoid input modification due
        # to upcoming in-place operations.
        dequant = input.to(torch.int32, copy=True)
        if zero_point is not None:
            dequant = dequant - zero_point.to(torch.int32)
        dequant = dequant.to(output_dtype)
        dequant = dequant * scale
    elif zero_point_domain == ZeroPointDomain.NONE.name:
        assert zero_point is None, (
            "zero_point should be None when zero_point_domain is NONE"
        )
        dequant = input.to(output_dtype)
        dequant = dequant * scale
    elif zero_point_domain is None:
        # This case handles dequantization for float8 we expect no zero point and no zero point domain
        assert zero_point is None, (
            "zero_point should be None when zero_point_domain is None"
        )
        assert _is_float8_type(input.dtype), (
            f"dequantiztion with no zero point domain is only supported with FP8 types, got {input.dtype}"
        )
        dequant = input.to(output_dtype)
        dequant = dequant * scale
    else:
        assert zero_point_domain == ZeroPointDomain.FLOAT.name, (
            f"Unexpected zero point domain: {zero_point_domain}"
        )
        # TODO: this seems to be a detail for tinygemm (converting from uint to int, probably need to refactor this)
        mid_point = (quant_max + quant_min + 1) / 2
        # This should allocate new memory and avoid input modification
        dequant = input - mid_point
        dequant = dequant.to(output_dtype)
        dequant *= scale
        if zero_point is not None:
            dequant += zero_point

    return dequant.view(original_shape).to(output_dtype)
