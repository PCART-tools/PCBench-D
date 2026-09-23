def _compare_scalars_internal(a, b, *, rtol: float, atol: float, equal_nan: Union[str, bool]) -> _compare_return_type:
    def _helper(a, b, s) -> _compare_return_type:
        # Short-circuits on identity
        if a == b or ((equal_nan in {"relaxed", True}) and a != a and b != b):
            return (True, None)

        # Special-case for NaN comparisions when equal_nan=False
        if not (equal_nan in {"relaxed", True}) and (a != a or b != b):
            msg = ("Found {0} and {1} while comparing" + s + "and either one "
                   "is nan and the other isn't, or both are nan and "
                   "equal_nan is False").format(a, b)
            return (False, msg)

        diff = abs(a - b)
        allowed_diff = atol + rtol * abs(b)
        result = diff <= allowed_diff

        # Special-case for infinity comparisons
        # NOTE: if b is inf then allowed_diff will be inf when rtol is not 0
        if ((cmath.isinf(a) or cmath.isinf(b)) and a != b):
            result = False

        msg = None
        if not result:
            if rtol == 0 and atol == 0:
                msg = f"{a} != {b}"
            else:
                msg = (
                    f"Comparing{s}{a} and {b} gives a "
                    f"difference of {diff}, but the allowed difference "
                    f"with rtol={rtol} and atol={atol} is "
                    f"only {allowed_diff}!"
                )
        return result, msg

    return _helper(a, b, " ")
