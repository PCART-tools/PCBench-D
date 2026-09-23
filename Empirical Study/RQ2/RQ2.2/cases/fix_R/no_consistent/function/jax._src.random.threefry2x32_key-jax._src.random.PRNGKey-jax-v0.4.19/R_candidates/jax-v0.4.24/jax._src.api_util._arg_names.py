def _arg_names(fn, args, kwargs, static_argnums, static_argnames,
               ) -> tuple[str, ...] | None:
  static = object()
  static_argnums_ = _ensure_inbounds(True, len(args), static_argnums)
  static_argnames_ = set(static_argnames)
  args_ = [static if i in static_argnums_ else x for i, x in enumerate(args)]
  kwargs = {k:static if k in static_argnames_ else x for k, x in kwargs.items()}
  try:
    ba = inspect.signature(fn).bind(*args_, **kwargs)
  except (ValueError, TypeError):
    return None
  return tuple(f'{name}{keystr(path)}' for name, x in ba.arguments.items()
               for path, l in generate_key_paths(x) if l is not static)
