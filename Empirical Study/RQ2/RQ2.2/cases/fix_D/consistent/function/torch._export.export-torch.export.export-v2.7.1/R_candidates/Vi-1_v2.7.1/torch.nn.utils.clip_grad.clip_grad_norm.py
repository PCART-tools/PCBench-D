@deprecated(
    "`torch.nn.utils.clip_grad_norm` is now deprecated "
    "in favor of `torch.nn.utils.clip_grad_norm_`.",
    category=FutureWarning,
)
def clip_grad_norm(
    parameters: _tensor_or_tensors,
    max_norm: float,
    norm_type: float = 2.0,
    error_if_nonfinite: bool = False,
    foreach: Optional[bool] = None,
) -> torch.Tensor:
    r"""Clip the gradient norm of an iterable of parameters.

    .. warning::
        This method is now deprecated in favor of
        :func:`torch.nn.utils.clip_grad_norm_`.
    """
    return clip_grad_norm_(parameters, max_norm, norm_type, error_if_nonfinite, foreach)
