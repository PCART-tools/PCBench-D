@util._wraps(np.diagonal, lax_description=_ARRAY_VIEW_DOC)
@partial(jit, static_argnames=('offset', 'axis1', 'axis2'))
def diagonal(a, offset=0, axis1: int = 0, axis2: int = 1):
  util.check_arraylike("diagonal", a)
  a_shape = shape(a)
  if ndim(a) < 2:
    raise ValueError("diagonal requires an array of at least two dimensions.")
  offset = core.concrete_or_error(operator.index, offset, "'offset' argument of jnp.diagonal()")

  a = moveaxis(a, (axis1, axis2), (-2, -1))

  diag_size = max(0, min(a_shape[axis1] + min(offset, 0),
                         a_shape[axis2] - max(offset, 0)))
  i = arange(diag_size)
  j = arange(abs(offset), abs(offset) + diag_size)
  return a[..., i, j] if offset >= 0 else a[..., j, i]
