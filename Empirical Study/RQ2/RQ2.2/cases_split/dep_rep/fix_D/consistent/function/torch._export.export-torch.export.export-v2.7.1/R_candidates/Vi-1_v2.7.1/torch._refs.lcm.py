@_make_elementwise_binary_reference(
    type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    supports_lhs_python_scalar=False,
    supports_rhs_python_scalar=False,
)
def lcm(a: TensorLikeType, b: TensorLikeType):
    dtype = a.dtype
    # promoting to int32 to maintain 100% consistency with C++ and to
    # prevent overflow in case of int8 and int16
    promote_to_int = dtype in (torch.int8, torch.int16)
    if promote_to_int:
        a = prims.convert_element_type(a, torch.int32)
        b = prims.convert_element_type(b, torch.int32)

    g = torch.gcd(a, b)
    # Avoid division by zero in case gcd(0, 0) == 0
    g = torch.where(g == 0, 1, g)
    res = torch.abs(prims.div(a, g) * b)
    return res if not promote_to_int else prims.convert_element_type(res, dtype)
