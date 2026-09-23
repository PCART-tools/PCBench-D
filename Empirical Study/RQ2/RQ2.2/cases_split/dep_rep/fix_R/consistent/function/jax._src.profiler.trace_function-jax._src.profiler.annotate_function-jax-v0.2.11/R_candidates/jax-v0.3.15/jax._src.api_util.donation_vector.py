def donation_vector(donate_argnums, args, kwargs) -> Tuple[bool, ...]:
  """Returns a tuple with a boolean value for each leaf in args."""
  res = []
  for i, arg in enumerate(args):
    donate = bool(i in donate_argnums)
    res.extend((donate,) * tree_structure(arg).num_leaves)
  res.extend((False,) * tree_structure(kwargs).num_leaves)
  return tuple(res)
