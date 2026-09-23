def choose_qparams_affine_with_min_max(
    min_val: torch.Tensor,
    max_val: torch.Tensor,
    mapping_type: MappingType,
    block_size: tuple[int, ...],
    target_dtype: torch.dtype,
    quant_min: Optional[int] = None,
    quant_max: Optional[int] = None,
    eps: Optional[float] = None,
    scale_dtype: Optional[torch.dtype] = None,
    zero_point_dtype: Optional[torch.dtype] = None,
    preserve_zero: bool = True,
    zero_point_domain: Optional[ZeroPointDomain] = ZeroPointDomain.INT,
) -> tuple[torch.Tensor, torch.Tensor]:
    """A variant of :func:`~torchao.quantization.quant_primitives.choose_qparams_affine`
    operator that pass in min_val and max_val directly instead of deriving these from a single input.
    This is used for observers in static quantization where min_val and max_val may be obtained through
    tracking all the data in calibration data set.

    Args:
      Mostly same as :func:`~torchao.quantization.quant_primitives.choose_qparams_affine`. with one
      difference: instead of passing in `input` Tensor and use that to calculate min_val/max_val
      and then scale/zero_point, we pass in min_val/max_val directly
    """
    return _choose_qparams_affine(
        None,
        mapping_type.name,
        block_size,
        target_dtype,
        quant_min,
        quant_max,
        eps,
        scale_dtype,
        zero_point_dtype,
        preserve_zero,
        zero_point_domain.name if zero_point_domain is not None else None,
        min_val,
        max_val,
    )
