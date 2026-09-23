@register_meta(aten.sigmoid)
@out_wrapper()
def sigmoid(self: Tensor) -> Tensor:
    _, result_dtype = elementwise_dtypes(
        self,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
    )
    return torch.empty_like(self, dtype=result_dtype)
