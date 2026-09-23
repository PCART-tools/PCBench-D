def _warn_on_positional_kwargs(f):
  """Decorator used for backward compatibility of keyword-only arguments.

  Some functions were changed to mark their keyword arguments as keyword-only.
  This decorator allows existing code to keep working temporarily, while issuing
  a warning if a now keyword-only parameter is passed positionally."""
  sig = inspect.signature(f)
  pos_names = [name for name, p in sig.parameters.items()
               if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD]
  kwarg_names = [name for name, p in sig.parameters.items()
                 if p.kind == inspect.Parameter.KEYWORD_ONLY]

  # This decorator assumes that all arguments to `f` are either
  # positional-or-keyword or keyword-only.
  assert len(pos_names) + len(kwarg_names) == len(sig.parameters)

  @functools.wraps(f)
  def wrapped(*args, **kwargs):
    if len(args) < len(pos_names):
      a = pos_names[len(args)]
      raise TypeError(f"{f.__name__} missing required positional argument: {a}")

    pos_args = args[:len(pos_names)]
    extra_kwargs = args[len(pos_names):]

    if len(extra_kwargs) > len(kwarg_names):
      raise TypeError(f"{f.__name__} takes at most {len(sig.parameters)} "
                      f" arguments but {len(args)} were given.")

    for name, value in zip(kwarg_names, extra_kwargs):
      if name in kwargs:
        raise TypeError(f"{f.__name__} got multiple values for argument: "
                        f"{name}")

      warnings.warn(f"Argument {name} to {f.__name__} is now a keyword-only "
                    "argument. Support for passing it positionally will be "
                    "removed in an upcoming JAX release.",
                    DeprecationWarning)
      kwargs[name] = value
    return f(*pos_args, **kwargs)

  return wrapped
