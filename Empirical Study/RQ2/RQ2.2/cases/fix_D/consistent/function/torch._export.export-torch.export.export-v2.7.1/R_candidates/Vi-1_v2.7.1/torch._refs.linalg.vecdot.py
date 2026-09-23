@out_wrapper()
@elementwise_type_promotion_wrapper(
    type_promoting_args=("x", "y"),
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
)
def vecdot(x: Tensor, y: Tensor, dim: int = -1) -> Tensor:
    check_fp_or_complex(x.dtype, "linalg.vecdot")
    return (x.conj() * y).sum(dim=dim)
