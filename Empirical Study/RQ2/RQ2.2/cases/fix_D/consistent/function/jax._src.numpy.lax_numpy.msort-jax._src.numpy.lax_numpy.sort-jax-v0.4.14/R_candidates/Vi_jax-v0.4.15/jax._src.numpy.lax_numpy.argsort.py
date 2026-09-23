@util._wraps(np.argsort, lax_description=_ARGSORT_DOC)
@partial(jit, static_argnames=('axis', 'kind', 'order'))
def argsort(
    a: ArrayLike,
    axis: int | None = -1,
    kind: str = "stable",
    order: None = None,
) -> Array:
  util.check_arraylike("argsort", a)
  arr = asarray(a)
  if kind != 'stable':
    warnings.warn("'kind' argument to argsort is ignored; only 'stable' sorts "
                  "are supported.")
  if order is not None:
    raise ValueError("'order' argument to argsort is not supported.")

  if axis is None:
    return argsort(arr.ravel(), 0)
  else:
    axis_num = _canonicalize_axis(axis, arr.ndim)
    use_64bit_index = not core.is_constant_dim(arr.shape[axis_num]) or arr.shape[axis_num] >= (1 << 31)
    iota = lax.broadcasted_iota(int64 if use_64bit_index else int_, arr.shape, axis_num)
    _, perm = lax.sort_key_val(arr, iota, dimension=axis_num)
    return perm
