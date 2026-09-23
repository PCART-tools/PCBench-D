def argnums_partial_except(f: lu.WrappedFun, static_argnums: Tuple[int, ...],
                           args: Tuple[Any], *, allow_invalid: bool):
  """Version of ``argnums_partial`` that checks hashability of static_argnums."""
  if not static_argnums:
    return f, args
  static_argnums = _ensure_inbounds(allow_invalid, len(args), static_argnums)
  dyn_argnums = tuple(i for i in range(len(args)) if i not in static_argnums)
  dyn_args = tuple(args[i] for i in dyn_argnums)

  fixed_args = []
  for i in static_argnums:
    # TODO(shoyer): set allow_invalid=True permanently after static_argnames.
    if allow_invalid and i >= len(args):
      continue
    static_arg = args[i]
    if not is_hashable(static_arg):
      raise ValueError(
          "Non-hashable static arguments are not supported, as this can lead "
          f"to unexpected cache-misses. Static argument (index {i}) of type "
          f"{type(static_arg)} for function {f.__name__} is non-hashable.")
    else:
      fixed_args.append(_HashableWithStrictTypeEquality(static_arg))  # type: ignore

  return _argnums_partial(f, dyn_argnums, tuple(fixed_args)), dyn_args
