@implements(np.nanquantile, skip_params=['out', 'overwrite_input'])
@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'interpolation', 'keepdims', 'method'))
def nanquantile(a: ArrayLike, q: ArrayLike, axis: int | tuple[int, ...] | None = None,
                out: None = None, overwrite_input: bool = False, method: str = "linear",
                keepdims: bool = False, *, interpolation: DeprecatedArg | str = DeprecatedArg()) -> Array:
  check_arraylike("nanquantile", a, q)
  if overwrite_input or out is not None:
    msg = ("jax.numpy.nanquantile does not support overwrite_input=True or "
           "out != None")
    raise ValueError(msg)
  if not isinstance(interpolation, DeprecatedArg):
    warnings.warn("The interpolation= argument to 'nanquantile' is deprecated. "
                  "Use 'method=' instead.", DeprecationWarning, stacklevel=2)
    method = interpolation
  return _quantile(lax_internal.asarray(a), lax_internal.asarray(q), axis, method, keepdims, True)
