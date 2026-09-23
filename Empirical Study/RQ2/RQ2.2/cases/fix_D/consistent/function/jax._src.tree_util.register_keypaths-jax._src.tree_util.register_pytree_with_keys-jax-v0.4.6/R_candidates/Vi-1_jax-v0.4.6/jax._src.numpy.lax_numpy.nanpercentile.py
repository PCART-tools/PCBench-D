@util._wraps(np.nanpercentile, skip_params=['out', 'overwrite_input'])
@partial(jit, static_argnames=('axis', 'overwrite_input', 'interpolation',
                               'keepdims', 'method'))
def nanpercentile(a: ArrayLike, q: ArrayLike,
                  axis: Optional[Union[int, Tuple[int, ...]]] = None,
                  out: None = None, overwrite_input: bool = False, method: str = "linear",
                  keepdims: bool = False, interpolation: None = None) -> Array:
  util._check_arraylike("nanpercentile", a, q)
  q = ufuncs.true_divide(q, float32(100.0))
  return nanquantile(a, q, axis=axis, out=out, overwrite_input=overwrite_input,
                     interpolation=interpolation, method=method,
                     keepdims=keepdims)
