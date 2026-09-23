def allow_pass_by_position_with_warning(f):
  @wraps(f)
  def wrapped(*args, **kwargs):
    sig = inspect.signature(f)
    try:
      sig.bind(*args, **kwargs)
    except TypeError:
      argspec = inspect.getfullargspec(f)
      n_positional = len(argspec.args)
      keywords = argspec.kwonlyargs[:len(args) - n_positional]
      warnings.warn(
          f"jnp.ndarray.at[...].{f.__name__}: Passing '{keywords[0]}' by position is deprecated. "
          f"Pass by keyword instead", category=FutureWarning, stacklevel=2)
      converted_kwargs = dict(zip(keywords, args[n_positional:]))
      return f(*args[:n_positional], **converted_kwargs, **kwargs)
    else:
      return f(*args, **kwargs)
  return wrapped
