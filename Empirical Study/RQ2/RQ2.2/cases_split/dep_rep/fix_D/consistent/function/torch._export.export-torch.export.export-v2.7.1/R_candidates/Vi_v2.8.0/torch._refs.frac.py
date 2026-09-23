@_make_elementwise_unary_reference(
    ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    exact_dtype=True,
)
def frac(x: TensorLikeType) -> TensorLikeType:
    trunc_x = torch.mul(torch.floor(torch.abs(x)), torch.sign(x))
    return torch.sub(x, trunc_x)
