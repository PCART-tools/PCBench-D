def argnames_partial_except(f: lu.WrappedFun, static_argnames: tuple[str, ...],
                            kwargs: dict[str, Any]):
  if not static_argnames:
    return f, kwargs
  dyn_kwargs = {k: v for k, v in kwargs.items() if k not in static_argnames}

  fixed_kwargs: dict[str, Any] = {}
  for k, arg in kwargs.items():
    if k not in dyn_kwargs:
      try:
        hash(arg)
      except TypeError:
        raise ValueError(
            "Non-hashable static arguments are not supported, as this can lead "
            f"to unexpected cache-misses. Static argument (name {k}) of type "
            f"{type(arg)} for function {f.__name__} is non-hashable.")
      else:
        fixed_kwargs[k] = Hashable(arg)  # type: ignore

  return _argnames_partial(f, WrapKwArgs(fixed_kwargs)), dyn_kwargs
