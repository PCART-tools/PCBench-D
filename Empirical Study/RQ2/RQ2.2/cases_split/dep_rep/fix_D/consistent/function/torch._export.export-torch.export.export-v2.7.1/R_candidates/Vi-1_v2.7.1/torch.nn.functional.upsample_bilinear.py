def upsample_bilinear(input, size=None, scale_factor=None):  # noqa: F811
    r"""Upsamples the input, using bilinear upsampling.

    .. warning::
        This function is deprecated in favor of :func:`torch.nn.functional.interpolate`.
        This is equivalent with
        ``nn.functional.interpolate(..., mode='bilinear', align_corners=True)``.

    Expected inputs are spatial (4 dimensional). Use `upsample_trilinear` fo
    volumetric (5 dimensional) inputs.

    Args:
        input (Tensor): input
        size (int or Tuple[int, int]): output spatial size.
        scale_factor (int or Tuple[int, int]): multiplier for spatial size

    Note:
        {backward_reproducibility_note}
    """
    # DeprecationWarning is ignored by default
    warnings.warn(
        "`nn.functional.upsample_bilinear` is deprecated. "
        "Use `nn.functional.interpolate` instead.",
        stacklevel=2,
    )
    return interpolate(input, size, scale_factor, mode="bilinear", align_corners=True)
