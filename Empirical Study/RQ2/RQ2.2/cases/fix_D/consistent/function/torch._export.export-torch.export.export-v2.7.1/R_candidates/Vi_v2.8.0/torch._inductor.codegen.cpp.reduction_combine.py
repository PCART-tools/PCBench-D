def reduction_combine(
    reduction_type,
    var,
    next_value,
    index: Optional[sympy.Symbol] = None,
    src_dtype=None,
):
    is_bool = src_dtype == torch.bool
    if reduction_type == "sum":
        conjunction = "|" if is_bool else "+"
        return f"{var} {conjunction} {next_value}"
    if reduction_type == "prod":
        return f"{var} * {next_value}"
    if reduction_type == "xor_sum":
        return f"{var} ^ {next_value}"
    if reduction_type == "any":
        return f"{var} || {next_value}"
    if reduction_type in ("min", "max"):
        return f"{reduction_type}_propagate_nan({var}, {next_value})"
    if reduction_type == "welford_reduce":
        return f"welford_combine({var}, {next_value})"
    if reduction_type == "welford_combine":
        if isinstance(next_value, tuple):
            mean, m2, weight = next_value
        else:
            mean, m2, weight = reduction_project(reduction_type, next_value)
        return f"welford_combine({var}, {{{mean}, {m2}, {weight}}})"
    if reduction_type in ("argmin", "argmax"):
        if (
            hasattr(next_value, "dtype")
            and next_value.dtype == torch.bool
            and not next_value.is_vec
        ):
            if index is not None:
                return f"{reduction_type}_combine({var}, static_cast<float>({next_value}), {index})"
            else:
                return (
                    f"{reduction_type}_combine({var}, static_cast<float>({next_value}))"
                )
        if index is not None:
            return f"{reduction_type}_combine({var}, {next_value}, {index})"
        else:
            return f"{reduction_type}_combine({var}, {next_value})"
    raise AssertionError(reduction_type)
