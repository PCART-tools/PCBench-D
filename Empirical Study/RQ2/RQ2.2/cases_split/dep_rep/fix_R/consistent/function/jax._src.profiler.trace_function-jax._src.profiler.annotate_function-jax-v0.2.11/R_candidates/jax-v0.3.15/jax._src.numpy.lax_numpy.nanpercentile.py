@_wraps(np.nanpercentile, skip_params=['out', 'overwrite_input'])
@partial(jit, static_argnames=('axis', 'overwrite_input', 'interpolation',
                               'keepdims', 'method'))
def nanpercentile(a, q, axis: Optional[Union[int, Tuple[int, ...]]] = None,
                  out=None, overwrite_input=False, method="linear",
                  keepdims=False, interpolation=None):
  _check_arraylike("nanpercentile", a, q)
  q = true_divide(q, float32(100.0))
  return nanquantile(a, q, axis=axis, out=out, overwrite_input=overwrite_input,
                     interpolation=interpolation, method=method,
                     keepdims=keepdims)
