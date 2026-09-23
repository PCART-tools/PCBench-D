def hinge_embedding_loss(
    input: Tensor,
    target: Tensor,
    margin: float = 1.0,
    size_average: Optional[bool] = None,
    reduce: Optional[bool] = None,
    reduction: str = "mean",
) -> Tensor:  # noqa: D400,D402
    r"""Compute the hinge embedding loss.

    See :class:`~torch.nn.HingeEmbeddingLoss` for details.

    Args:
       input (Tensor): Predicted values.
       target (Tensor): Ground truth values.
       margin (float, optional): Margin for hinge loss. Has a default value of 1.
       size_average (bool, optional): Deprecated (see :attr:`reduction`).
       reduce (bool, optional): Deprecated (see :attr:`reduction`).
       reduction (str, optional): Specifies the reduction to apply to the output:
                                  'none' | 'mean' | 'sum'. 'mean': the mean of the output is taken.
                                  'sum': the output will be summed. 'none': no reduction will be applied.
                                  Default: 'mean'.

    Returns:
       Tensor: Hinge embedding loss.
    """
    if has_torch_function_variadic(input, target):
        return handle_torch_function(
            hinge_embedding_loss,
            (input, target),
            input,
            target,
            margin=margin,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
        )
    if size_average is not None or reduce is not None:
        reduction_enum = _Reduction.legacy_get_enum(size_average, reduce)
    else:
        reduction_enum = _Reduction.get_enum(reduction)
    return torch.hinge_embedding_loss(input, target, margin, reduction_enum)
