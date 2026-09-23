def _outfeed_abstract_eval(token, *xs, partitions):
  if token is not abstract_token:
    raise TypeError("First argument to outfeed must be a token")
  return abstract_token
