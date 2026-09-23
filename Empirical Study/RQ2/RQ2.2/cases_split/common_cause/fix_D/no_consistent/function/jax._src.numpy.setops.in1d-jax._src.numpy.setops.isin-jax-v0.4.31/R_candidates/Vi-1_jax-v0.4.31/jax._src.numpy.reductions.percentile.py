@implements(np.percentile, skip_params=['out', 'overwrite_input'])
@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation', 'keepdims', 'method'))
def percentile(a: ArrayLike, q: ArrayLike,
               axis: int | tuple[int, ...] | None = None,
               out: None = None, overwrite_input: bool = False, method: str = "linear",
               keepdims: bool = False, *, interpolation: str | DeprecatedArg = DeprecatedArg()) -> Array:
  check_arraylike("percentile", a, q)
  q, = promote_dtypes_inexact(q)
  if not isinstance(interpolation, DeprecatedArg):
    warnings.warn("The interpolation= argument to 'percentile' is deprecated. "
                  "Use 'method=' instead.", DeprecationWarning, stacklevel=2)
    method = interpolation
  return quantile(a, q / 100, axis=axis, out=out, overwrite_input=overwrite_input,
                  method=method, keepdims=keepdims)
