@util._wraps(np.diagonal, lax_description=_ARRAY_VIEW_DOC)
@partial(jit, static_argnames=('offset', 'axis1', 'axis2'))
def diagonal(a, offset=0, axis1: int = 0, axis2: int = 1):
  util._check_arraylike("diagonal", a)
  a_shape = shape(a)
  if ndim(a) < 2:
    raise ValueError("diagonal requires an array of at least two dimensions.")
  offset = core.concrete_or_error(operator.index, offset, "'offset' argument of jnp.diagonal()")

  a = moveaxis(a, (axis1, axis2), (-2, -1))

  diag_size = _max(0, _min(a_shape[axis1] + _min(offset, 0),
                           a_shape[axis2] - _max(offset, 0)))
  i = arange(diag_size)
  j = arange(_abs(offset), _abs(offset) + diag_size)
  return a[..., i, j] if offset >= 0 else a[..., j, i]
