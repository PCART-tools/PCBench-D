def _limit_signed_rational(val, max_val, min_val):
    frac = Fraction(val)
    n_d = frac.numerator, frac.denominator

    if min(n_d) < min_val:
        n_d = _limit_rational(val, abs(min_val))

    if max(n_d) > max_val:
        val = Fraction(*n_d)
        n_d = _limit_rational(val, max_val)

    return n_d
