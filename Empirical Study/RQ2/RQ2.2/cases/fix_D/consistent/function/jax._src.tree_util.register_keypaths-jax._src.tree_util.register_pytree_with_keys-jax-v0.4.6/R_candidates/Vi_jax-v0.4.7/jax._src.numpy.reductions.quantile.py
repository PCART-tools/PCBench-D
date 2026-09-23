@_wraps(np.quantile, skip_params=['out', 'overwrite_input'])
@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation',
                               'keepdims', 'method'))
def quantile(a: ArrayLike, q: ArrayLike, axis: Optional[Union[int, Tuple[int, ...]]] = None,
             out: None = None, overwrite_input: bool = False, method: str = "linear",
             keepdims: bool = False, interpolation: None = None) -> Array:
  check_arraylike("quantile", a, q)
  if overwrite_input or out is not None:
    msg = ("jax.numpy.quantile does not support overwrite_input=True or "
           "out != None")
    raise ValueError(msg)
  if interpolation is not None:
    warnings.warn("The interpolation= argument to 'quantile' is deprecated. "
                  "Use 'method=' instead.", DeprecationWarning)
  return _quantile(_asarray(a), _asarray(q), axis, interpolation or method, keepdims, False)
