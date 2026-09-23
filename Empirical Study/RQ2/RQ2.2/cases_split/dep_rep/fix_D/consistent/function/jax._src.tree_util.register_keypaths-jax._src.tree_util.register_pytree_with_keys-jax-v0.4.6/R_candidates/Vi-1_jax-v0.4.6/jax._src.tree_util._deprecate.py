def _deprecate(f):
  @functools.wraps(f)
  def wrapped(*args, **kwargs):
    warnings.warn(f"jax.{f.__name__} is deprecated, and will be removed in a future release. "
                  f"Use jax.tree_util.{f.__name__} instead.",
                  category=FutureWarning, stacklevel=2)
    return f(*args, **kwargs)
  return wrapped
