def _apply_excluded(func, excluded, args):
  """Partially apply positional arguments in `excluded` to a function."""
  if not excluded:
    return func, args

  if max(excluded) >= len(args):
    raise ValueError("excluded={!r} is invalid for {!r} argument(s)"
                     .format(excluded, len(args)))

  dynamic_args = [arg for i, arg in enumerate(args) if i not in excluded]
  static_args = [(i, args[i]) for i in sorted(excluded)]

  def new_func(*args):
    args = list(args)
    for i, arg in static_args:
      args.insert(i, arg)
    return func(*args)

  return new_func, dynamic_args
