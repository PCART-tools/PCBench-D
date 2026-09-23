def donation_vector(donate_argnums, donate_argnames, args, kwargs) -> tuple[bool, ...]:
  """Returns a tuple with a boolean value for each leaf in args and kwargs.

  What if a user specifies donate_argnums but calls the function with kwargs
  or vice-versa? In that case, in `resolve_argnums` using the signature of the
  function, the counterpart (donate_argnames or donate_argnums respectively) is
  calculated so when this function is called both donate_argnums and
  donate_argnames are available. This allows JAX to donate kwargs when only
  donate_argnums is specified and vice-versa.

  When both donate_argnums and donate_argnames are specified, only the args and
  kwargs specified are donated.
  """
  res: list[bool] = []
  for i, arg in enumerate(args):
    donate = bool(i in donate_argnums)
    res.extend((donate,) * tree_structure(arg).num_leaves)
  for key, val in kwargs.items():
    donate = key in donate_argnames
    res.extend((donate,) * tree_structure(val).num_leaves)
  return tuple(res)
