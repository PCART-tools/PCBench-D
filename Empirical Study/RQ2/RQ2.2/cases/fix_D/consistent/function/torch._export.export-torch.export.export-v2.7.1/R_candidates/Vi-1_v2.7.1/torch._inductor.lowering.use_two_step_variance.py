def use_two_step_variance(x, axis, keepdim):
    # Instead of unrolling welford, just unroll the simpler two-step var
    axis = _validate_reduction_axis(x, axis)
    kwargs = _make_reduction_inner(
        x, axis=axis, keepdims=keepdim, dtype=None, override_return_dtype=None
    )

    ranges = kwargs["ranges"]
    reduction_numel = sympy_product(kwargs["reduction_ranges"])
    return (
        isinstance(reduction_numel, sympy.Integer)
        and int(reduction_numel) < config.unroll_reductions_threshold
        and sympy_product(ranges) != 1
    )
