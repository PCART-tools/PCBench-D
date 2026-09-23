def random_unwrap(keys):
  if not isinstance(keys, PRNGKeyArray):
    raise TypeError(f'random_unwrap takes key array operand, got {type(keys)}')
  return random_unwrap_p.bind(keys)
