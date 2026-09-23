def foreach_lerp_inplace(self, end, weight):
    # decompose foreach lerp into constituent ops, prevents a graph break due to
    # converting a value to a scalar when arg[2] is a single tensor
    result = torch._foreach_sub(end, self)
    result = torch._foreach_mul(result, weight)
    return torch._foreach_add_(self, result)
