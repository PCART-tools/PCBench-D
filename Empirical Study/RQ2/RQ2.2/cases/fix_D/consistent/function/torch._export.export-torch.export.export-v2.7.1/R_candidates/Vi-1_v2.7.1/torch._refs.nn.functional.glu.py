@register_decomposition(aten.glu)
@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("a",),
    type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def glu(a: TensorLikeType, dim: int = -1) -> TensorLikeType:
    dim = utils.canonicalize_dims(a.ndim, dim)
    torch._check(
        a.shape[dim] % 2 == 0,
        lambda: f"Halving dimension must be even, but dimension {dim} is size {a.shape[dim]}",
    )
    b, c = torch.tensor_split(a, 2, dim)

    return b * torch.sigmoid(c)
