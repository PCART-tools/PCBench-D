@util._wraps(np.sort)
@partial(jit, static_argnames=('axis', 'kind', 'order'))
def sort(a, axis: Optional[int] = -1, kind='quicksort', order=None):
  util.check_arraylike("sort", a)
  if kind != 'quicksort':
    warnings.warn("'kind' argument to sort is ignored.")
  if order is not None:
    raise ValueError("'order' argument to sort is not supported.")

  if axis is None:
    return lax.sort(ravel(a), dimension=0)
  else:
    return lax.sort(asarray(a), dimension=_canonicalize_axis(axis, ndim(a)))
