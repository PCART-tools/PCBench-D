@implements(np.nanquantile, skip_params=['out', 'overwrite_input'])
@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation',
                               'keepdims', 'method'))
def nanquantile(a: ArrayLike, q: ArrayLike, axis: int | tuple[int, ...] | None = None,
                out: None = None, overwrite_input: bool = False, method: str = "linear",
                keepdims: bool = False, interpolation: None = None) -> Array:
  check_arraylike("nanquantile", a, q)
  if overwrite_input or out is not None:
    msg = ("jax.numpy.nanquantile does not support overwrite_input=True or "
           "out != None")
    raise ValueError(msg)
  if interpolation is not None:
    warnings.warn("The interpolation= argument to 'nanquantile' is deprecated. "
                  "Use 'method=' instead.", DeprecationWarning)
  return _quantile(lax_internal.asarray(a), lax_internal.asarray(q), axis, interpolation or method, keepdims, True)
