@register_decomposition(aten.logsumexp)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("self",),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
)
def logsumexp(
    self: TensorLikeType, dim: DimsType, keepdim: bool = False
) -> TensorLikeType:
    if not isinstance(dim, Iterable):
        dim = (dim,)
    if self.numel() == 0:
        return torch.sum(torch.exp(self), dim, keepdim).log()
    maxes = torch.amax(torch.real(self), dim, keepdim=True)
    maxes = torch.masked_fill(maxes, maxes.abs() == float("inf"), 0)
    maxes_squeezed = maxes if keepdim else torch.squeeze(maxes, dim)
    result = torch.sum(torch.exp(self - maxes), dim, keepdim)
    return result.log().add(maxes_squeezed)
