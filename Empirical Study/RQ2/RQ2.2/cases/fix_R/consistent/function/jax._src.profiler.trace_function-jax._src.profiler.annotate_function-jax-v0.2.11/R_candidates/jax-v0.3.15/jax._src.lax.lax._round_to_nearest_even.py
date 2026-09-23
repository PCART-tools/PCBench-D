def _round_to_nearest_even(x):
  half = _const(x, 0.5)
  one = _const(x, 1)
  round_val = floor(x)
  fraction = x - round_val
  nearest_even_int = sub(
    round_val, mul(_const(x, 2), floor(mul(half, x))))
  is_odd = eq(nearest_even_int, one)
  return select(
    bitwise_or(gt(fraction, half),
               bitwise_and(eq(fraction, half), is_odd)),
    add(round_val, one), round_val)
