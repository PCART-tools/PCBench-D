def max_contiguous(x, values):
  if not isinstance(values, list):
    values = [values]
  return max_contiguous_p.bind(x, values=values)
