@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    supports_lhs_python_scalar=False,
    supports_rhs_python_scalar=False,
)
def heaviside(input: TensorLikeType, values: TensorLikeType) -> TensorLikeType:
    input_eq_zero = torch.eq(input, 0)
    input_lt_zero = torch.logical_or(torch.lt(input, 0), torch.isnan(input))
    zeros_and_ones = torch.where(input_lt_zero, 0, 1)
    output = torch.where(input_eq_zero, values, zeros_and_ones)
    return output
