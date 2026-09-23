@functools.cache
def get_k_splits(m: _IntLike, n: _IntLike, k: _IntLike) -> list[int]:
    # If k is a sympy expression, we can't do any splitting
    if isinstance(k, sympy.Expr) and not k.is_number:
        return default_k_splits

    if (isinstance(m, sympy.Expr) and not m.is_number) or (
        isinstance(n, sympy.Expr) and not n.is_number
    ):
        max_k_split = 256
    else:
        max_k_split = min(k // m, k // n)

    min_k_split = 2
    # Get all divisors of k, k has to be divisible by kPart
    divisors = sympy.divisors(k)

    divisors = [
        divisor
        for divisor in divisors
        if divisor <= max_k_split and divisor >= min_k_split
    ]

    pow_of_2_divisors, mul_of_32_divisors, rest_of_splits = [], [], []

    for d in divisors:
        kPart = k // d

        # Smaller than 128 might not even fit in a single tile, BLOCK_K can be 128
        if kPart < 128:
            continue

        # Power of 2 divisors are best performing, conform to hardware
        if (kPart & kPart - 1) == 0 and kPart >= 128:
            pow_of_2_divisors.append(d)
        # Else check if creates a multiple of 32
        elif kPart % 32 == 0:
            mul_of_32_divisors.append(d)
        # otherwise, take the smallest values
        else:
            rest_of_splits.append(d)

    if config.max_autotune_gemm_search_space == "EXHAUSTIVE":
        return pow_of_2_divisors + mul_of_32_divisors + rest_of_splits
    # If the # of power of 2 divisors are greater than k_splits_limit, return all
    # This should be ok for compile time, all perfect squares between 128 and min(k / m, k / n)
    # should never be a massive amount
    if len(pow_of_2_divisors) >= k_splits_limit:
        return pow_of_2_divisors
    else:
        best_splits = pow_of_2_divisors + mul_of_32_divisors + rest_of_splits
        # Otherwise, conform results to k_splits_limit
        return best_splits[:k_splits_limit]
