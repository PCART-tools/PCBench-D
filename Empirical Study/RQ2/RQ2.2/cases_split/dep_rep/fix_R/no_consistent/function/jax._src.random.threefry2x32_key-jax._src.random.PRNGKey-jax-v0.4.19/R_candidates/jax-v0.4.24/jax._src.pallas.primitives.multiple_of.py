def multiple_of(x, values):
  if not isinstance(values, list):
    values = [values]
  return multiple_of_p.bind(x, values=values)
