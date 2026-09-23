@util._wraps(np.argsort, lax_description=_ARGSORT_DOC)
@partial(jit, static_argnames=('axis', 'kind', 'order'))
def argsort(a, axis: Optional[int] = -1, kind='stable', order=None):
  util._check_arraylike("argsort", a)
  if kind != 'stable':
    warnings.warn("'kind' argument to argsort is ignored; only 'stable' sorts "
                  "are supported.")
  if order is not None:
    raise ValueError("'order' argument to argsort is not supported.")

  if axis is None:
    return argsort(a.ravel(), 0)
  else:
    axis_num = _canonicalize_axis(axis, ndim(a))
    use_64bit_index = core.is_special_dim_size(a.shape[axis_num]) or a.shape[axis_num] >= (1 << 31)
    iota = lax.broadcasted_iota(int64 if use_64bit_index else int_, shape(a), axis_num)
    _, perm = lax.sort_key_val(a, iota, dimension=axis_num)
    return perm
