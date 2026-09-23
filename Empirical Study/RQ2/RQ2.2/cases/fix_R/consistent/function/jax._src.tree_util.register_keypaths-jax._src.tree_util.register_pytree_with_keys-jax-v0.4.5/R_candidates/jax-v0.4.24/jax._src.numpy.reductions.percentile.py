@implements(np.percentile, skip_params=['out', 'overwrite_input'])
@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation',
                                   'keepdims', 'method'))
def percentile(a: ArrayLike, q: ArrayLike,
               axis: int | tuple[int, ...] | None = None,
               out: None = None, overwrite_input: bool = False, method: str = "linear",
               keepdims: bool = False, interpolation: None = None) -> Array:
  check_arraylike("percentile", a, q)
  q, = promote_dtypes_inexact(q)
  return quantile(a, q / 100, axis=axis, out=out, overwrite_input=overwrite_input,
                  interpolation=interpolation, method=method, keepdims=keepdims)
