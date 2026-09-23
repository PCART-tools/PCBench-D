@_wraps(np.trace, skip_params=['out'])
@partial(jit, static_argnames=('offset', 'axis1', 'axis2', 'dtype'))
def trace(a, offset=0, axis1: int = 0, axis2: int = 1, dtype=None, out=None):
  _check_arraylike("trace", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.trace is not supported.")
  lax_internal._check_user_dtype_supported(dtype, "trace")

  a_shape = shape(a)
  if dtype is None:
    dtype = _dtype(a)
    if issubdtype(dtype, integer):
      default_int = dtypes.canonicalize_dtype(np.int_)
      if iinfo(dtype).bits < iinfo(default_int).bits:
        dtype = default_int

  a = moveaxis(a, (axis1, axis2), (-2, -1))

  # Mask out the diagonal and reduce.
  a = where(eye(a_shape[axis1], a_shape[axis2], k=offset, dtype=bool),
            a, zeros_like(a))
  return sum(a, axis=(-2, -1), dtype=dtype)
