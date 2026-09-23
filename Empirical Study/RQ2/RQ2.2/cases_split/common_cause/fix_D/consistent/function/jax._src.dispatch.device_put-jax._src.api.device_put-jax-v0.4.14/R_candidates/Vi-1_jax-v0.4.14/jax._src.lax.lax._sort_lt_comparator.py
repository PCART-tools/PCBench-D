def _sort_lt_comparator(*operands, num_keys=1):
  x_keys, y_keys = _operands_to_keys(*operands, num_keys=num_keys)
  p = None
  for xk, yk in zip(x_keys[::-1], y_keys[::-1]):
    p = (bitwise_or(lt(xk, yk), bitwise_and(eq(xk, yk), p)) if p is not None
         else lt(xk, yk))
  return p
