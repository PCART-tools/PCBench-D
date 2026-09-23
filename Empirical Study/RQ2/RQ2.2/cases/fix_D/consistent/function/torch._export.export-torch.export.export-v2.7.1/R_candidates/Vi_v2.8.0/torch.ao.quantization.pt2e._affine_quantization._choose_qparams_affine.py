@register_custom_op
def _choose_qparams_affine(
    input: Optional[torch.Tensor],
    mapping_type: str,
    block_size: list[int],
    target_dtype: torch.dtype,
    quant_min: Optional[Union[int, float, bool]] = None,
    quant_max: Optional[Union[int, float, bool]] = None,
    eps: Optional[float] = None,
    scale_dtype: Optional[torch.dtype] = None,
    zero_point_dtype: Optional[torch.dtype] = None,
    preserve_zero: bool = True,
    zero_point_domain: Optional[str] = "INT",
    min_val: Optional[torch.Tensor] = None,
    max_val: Optional[torch.Tensor] = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """op definition that has compatible signatures with custom op library

    The op does the following:
    1. figure out the dimension for reduction based on block_size
    2. find min_val/max_val based on the dimension for reduction
    3. calculate quantization parameters based on min_val/max_val based on args like `preserve_zero`
       and `zero_point_domain`
    """
    quant_min, quant_max = _get_and_check_qmin_qmax(target_dtype, quant_min, quant_max)
    assert mapping_type in [
        MappingType.SYMMETRIC.name,
        MappingType.SYMMETRIC_NO_CLIPPING_ERR.name,
        MappingType.ASYMMETRIC.name,
    ], f"Unsupported mapping type: {mapping_type}"
    if target_dtype in FP8_TYPES:
        assert mapping_type == MappingType.SYMMETRIC.name, (
            f"Only symmetric quantization is supported for FP8 types, got {mapping_type}"
        )

    if input is not None:
        if scale_dtype is None:
            scale_dtype = input.dtype
        if zero_point_dtype is None:
            zero_point_dtype = input.dtype
        if eps is None:
            eps = torch.finfo(input.dtype).eps

        assert len(block_size) == input.dim(), (
            f"Got input dim:{input.dim()}, block_size: {block_size}"
        )
        shape_for_reduction, reduction_dims = _get_reduction_params(
            block_size, input.size()
        )
        input = input.view(shape_for_reduction)

        min_val = torch.amin(input, dim=reduction_dims, keepdim=False)
        max_val = torch.amax(input, dim=reduction_dims, keepdim=False)
    else:
        assert min_val is not None and max_val is not None, (
            "Need to provide `min_val` and `max_val` when `input` is None, got: {min_val, max_val}"
        )
        assert min_val.dtype == max_val.dtype, (
            "Expecting `min_val` and `max_val` to have the same dtype, got: {min_val.dtype, max_val.dtype}"
        )

        if scale_dtype is None:
            scale_dtype = min_val.dtype
        if zero_point_dtype is None:
            zero_point_dtype = min_val.dtype
        if eps is None:
            eps = torch.finfo(min_val.dtype).eps

    if preserve_zero:
        min_val_neg = torch.min(min_val, torch.zeros_like(min_val))
        max_val_pos = torch.max(max_val, torch.zeros_like(max_val))
    else:
        min_val_neg = min_val
        max_val_pos = max_val

    if (
        mapping_type == MappingType.SYMMETRIC.name
        or mapping_type == MappingType.SYMMETRIC_NO_CLIPPING_ERR.name
    ):
        # scales
        if mapping_type == MappingType.SYMMETRIC.name:
            max_val_pos = torch.max(-min_val_neg, max_val_pos)
            scale = max_val_pos / (float(quant_max - quant_min) / 2)
        else:
            assert mapping_type == MappingType.SYMMETRIC_NO_CLIPPING_ERR.name
            # calculate smin and smax individually and choose the larger one. For example, if quant_min = -8 and
            # quant_max = 7.
            # - If smin is bigger: There would be coverage on negative values down to -8, and less rounding
            # error than the existing SYMMETRIC case.
            # - If smax is bigger: it covers the positive values up to 7. The round
            # error may be bigger than the existing SYMMETRIC case. Either way, there's no out-of-range fp values after
            # quantization.
            smin = min_val_neg / float(quant_min)
            smax = max_val_pos / float(quant_max)
            mask = smin > smax
            scale = torch.where(mask, smin, smax)
        # zeros
        if not preserve_zero:
            raise ValueError(
                "preserve_zero == False is not supported for symmetric quantization"
            )
        if (
            zero_point_domain is not None
            and zero_point_domain != ZeroPointDomain.INT.name
        ):
            raise ValueError(
                "zero_point_domain != ZeroPointDomain.INT is not supported for symmetric quantization"
            )
        scale = torch.clamp(scale, min=eps)
        zero_point = torch.full_like(scale, int((quant_max + quant_min + 1) / 2))
    else:
        assert mapping_type == MappingType.ASYMMETRIC.name
        scale = (max_val_pos - min_val_neg) / float(quant_max - quant_min)
        scale = torch.clamp(scale, min=eps)
        if zero_point_domain == ZeroPointDomain.NONE.name:
            zero_point = None
        else:
            if preserve_zero:
                zero_point = quant_min - torch.round(min_val_neg / scale)
                zero_point = torch.clamp(zero_point, quant_min, quant_max)
            else:
                assert zero_point_domain == ZeroPointDomain.FLOAT.name, (
                    "if not preserve_zero, zero_point must be in FLOAT domain"
                )
                mid_point = (quant_max + quant_min + 1) / 2
                zero_point = min_val_neg + scale * mid_point

    if zero_point is not None:
        zero_point = zero_point.to(dtype=zero_point_dtype)
    return scale.to(dtype=scale_dtype), zero_point
