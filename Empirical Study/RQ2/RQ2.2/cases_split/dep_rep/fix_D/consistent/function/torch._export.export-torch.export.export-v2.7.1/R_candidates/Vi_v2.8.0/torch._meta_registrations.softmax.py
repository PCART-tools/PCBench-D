@register_meta(aten._softmax)
@out_wrapper()
def softmax(x: Tensor, dim: int, half_to_float: bool) -> Tensor:
    if half_to_float:
        assert x.dtype == torch.half
    computation_dtype, result_dtype = utils.elementwise_dtypes(
        x, type_promotion_kind=utils.ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )

    result_dtype = result_dtype if not half_to_float else computation_dtype
    res = torch.empty_like(x, dtype=result_dtype, memory_format=torch.contiguous_format)
    return res
