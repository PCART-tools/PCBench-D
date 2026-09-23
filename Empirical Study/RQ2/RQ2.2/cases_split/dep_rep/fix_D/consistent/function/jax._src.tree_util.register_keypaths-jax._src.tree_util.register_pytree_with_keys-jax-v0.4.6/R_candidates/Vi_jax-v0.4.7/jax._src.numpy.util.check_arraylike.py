def check_arraylike(fun_name: str, *args: Any):
  """Check if all args fit JAX's definition of arraylike."""
  assert isinstance(fun_name, str), f"fun_name must be a string. Got {fun_name}"
  if any(not _arraylike(arg) for arg in args):
    pos, arg = next((i, arg) for i, arg in enumerate(args)
                    if not _arraylike(arg))
    msg = "{} requires ndarray or scalar arguments, got {} at position {}."
    raise TypeError(msg.format(fun_name, type(arg), pos))
