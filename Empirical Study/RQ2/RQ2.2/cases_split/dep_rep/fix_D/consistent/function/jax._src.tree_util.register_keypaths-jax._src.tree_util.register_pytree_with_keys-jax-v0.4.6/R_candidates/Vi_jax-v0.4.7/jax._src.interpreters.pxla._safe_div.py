def _safe_div(x, y):
  result, ragged = divmod(x, y)
  assert not ragged, f"{x} % {y} != 0"
  return result
