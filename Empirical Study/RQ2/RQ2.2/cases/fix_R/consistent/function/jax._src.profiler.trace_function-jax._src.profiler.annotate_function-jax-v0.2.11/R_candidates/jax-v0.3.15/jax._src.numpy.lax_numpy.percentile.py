@_wraps(np.percentile, skip_params=['out', 'overwrite_input'])
@partial(jit, static_argnames=('axis', 'overwrite_input', 'interpolation',
                               'keepdims', 'method'))
def percentile(a, q, axis: Optional[Union[int, Tuple[int, ...]]] = None,
               out=None, overwrite_input=False, method="linear",
               keepdims=False, interpolation=None):
  _check_arraylike("percentile", a, q)
  q, = _promote_dtypes_inexact(q)
  return quantile(a, q / 100, axis=axis, out=out, overwrite_input=overwrite_input,
                  interpolation=interpolation, method=method, keepdims=keepdims)
