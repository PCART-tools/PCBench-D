def _infeed_abstract_eval(token, *, shapes, partitions):
  if token is not abstract_token:
    raise TypeError("First argument to infeed must be a token")
  return (*shapes, abstract_token), {infeed_effect}
