def wrap_init(f, params=None) -> WrappedFun:
  """Wraps function `f` as a `WrappedFun`, suitable for transformation."""
  params = () if params is None else tuple(sorted(params.items()))
  return WrappedFun(f, (), (), params, None)
