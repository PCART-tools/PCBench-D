@implements(np.nanpercentile, skip_params=['out', 'overwrite_input'])
@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation', 'keepdims', 'method'))
def nanpercentile(a: ArrayLike, q: ArrayLike,
                  axis: int | tuple[int, ...] | None = None,
                  out: None = None, overwrite_input: bool = False, method: str = "linear",
                  keepdims: bool = False, *, interpolation: str | DeprecatedArg = DeprecatedArg()) -> Array:
  check_arraylike("nanpercentile", a, q)
  q = ufuncs.true_divide(q, 100.0)
  if not isinstance(interpolation, DeprecatedArg):
    warnings.warn("The interpolation= argument to 'nanpercentile' is deprecated. "
                  "Use 'method=' instead.", DeprecationWarning, stacklevel=2)
    method = interpolation
  return nanquantile(a, q, axis=axis, out=out, overwrite_input=overwrite_input,
                     method=method, keepdims=keepdims)
