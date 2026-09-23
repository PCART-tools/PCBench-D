@_wraps(np.quantile, skip_params=['out', 'overwrite_input'])
@partial(jit, static_argnames=('axis', 'overwrite_input', 'interpolation',
                               'keepdims', 'method'))
def quantile(a, q, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
             overwrite_input=False, method="linear", keepdims=False,
             interpolation=None):
  _check_arraylike("quantile", a, q)
  if overwrite_input or out is not None:
    msg = ("jax.numpy.quantile does not support overwrite_input=True or "
           "out != None")
    raise ValueError(msg)
  if interpolation is not None:
    warnings.warn("The interpolation= argument to 'quantile' is deprecated. "
                  "Use 'method=' instead.", DeprecationWarning)
  return _quantile(a, q, axis, interpolation or method, keepdims, False)
