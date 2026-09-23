def _normalize(
    a: Tensor, norm_dims: DimsType, eps: float
) -> tuple[Tensor, Tensor, Tensor]:
    """Computes mean and 1/std of a tensor along norm_dims.

    Used as a helper function for normalization layers.

    Args:
        a (Tensor): input tensor
        norm_dims (DimsType): dimensions to normalize over
        eps (float): epsilon for numerical stability

    Returns:
        out (Tensor): normalized tensor.
        mean (Tensor): mean of the tensor along norm_dims.
        rstd (Tensor): 1/std of the tensor along norm_dims.
    """
    norm_dims = utils.canonicalize_dims(a.ndim, norm_dims)
    computation_dtype = utils.get_computation_dtype(a.dtype)
    a_acc = _maybe_convert_to_dtype(a, computation_dtype)
    assert isinstance(a_acc, TensorLike)  # to avoid mypy error for var_mean
    biased_var, mean = torch.var_mean(
        a_acc, dim=norm_dims, unbiased=False, keepdim=True
    )
    rstd = torch.rsqrt(biased_var + eps)
    out = (a_acc - mean) * rstd
    return out, mean, rstd
