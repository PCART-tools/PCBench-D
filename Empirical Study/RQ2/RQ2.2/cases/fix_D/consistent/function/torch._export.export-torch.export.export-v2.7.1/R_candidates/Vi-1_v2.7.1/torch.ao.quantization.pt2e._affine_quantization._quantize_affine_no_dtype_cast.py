def _quantize_affine_no_dtype_cast(
    input: torch.Tensor,
    block_size: list[int],
    scale: torch.Tensor,
    zero_point: Optional[torch.Tensor],
    quant_min: Union[int, float],
    quant_max: Union[int, float],
    zero_point_domain: Optional[str] = ZeroPointDomain.INT.name,
) -> torch.Tensor:
    """
    The op does the following:
    1. figure out the dimension for reduction based on block_size, also reshape the input to align with
       the shape after reduction
    2. quantize the input based on the quantization parameters scale and zero_point and args like zero_point_domain
    3. reshape the quantized result to origianl shape
    """
    # TODO: validations
    # TODO: validate scale/zero_point dimensions are compatible with block_size
    assert input.dtype in [
        torch.float32,
        torch.float16,
        torch.bfloat16,
    ], f"Unsupported input dtype: {input.dtype}"
    assert (
        len(block_size) == input.dim()
    ), f"Got input dim:{input.dim()}, block_size: {block_size}"
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
        quant = torch.clamp(
            torch.round(input * (1.0 / scale)) + zero_point, quant_min, quant_max
        )
    elif zero_point_domain == ZeroPointDomain.NONE.name:
        assert (
            zero_point is None
        ), "zero_point should be None when zero_point_domain is NONE"
        quant = torch.clamp(torch.round(input * (1.0 / scale)), quant_min, quant_max)
    elif zero_point_domain is None:
        # This case handles quantization for float8 we expect no zero point and no zero point domain
        assert (
            zero_point is None
        ), "zero_point should be None when zero_point_domain is None"
        quant = torch.clamp(input * scale.reciprocal(), quant_min, quant_max)
    else:
        assert zero_point_domain == ZeroPointDomain.FLOAT.name
        mid_point = (quant_max + quant_min + 1) / 2
        min_val = zero_point - scale * mid_point
        quant = torch.clamp(
            torch.round((input - min_val) / scale), quant_min, quant_max
        )
    quant = quant.view(original_shape)

    return quant
