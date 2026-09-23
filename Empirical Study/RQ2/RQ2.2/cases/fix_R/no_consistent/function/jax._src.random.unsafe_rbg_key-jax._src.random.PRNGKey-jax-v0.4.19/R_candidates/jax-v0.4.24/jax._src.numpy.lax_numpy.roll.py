@util.implements(np.roll)
def roll(a: ArrayLike, shift: ArrayLike | Sequence[int],
         axis: int | Sequence[int] | None = None) -> Array:
  util.check_arraylike("roll", a)
  arr = asarray(a)
  if axis is None:
    return roll(arr.ravel(), shift, 0).reshape(arr.shape)
  axis = _ensure_index_tuple(axis)
  axis = tuple(_canonicalize_axis(ax, arr.ndim) for ax in axis)
  try:
    shift = _ensure_index_tuple(shift)
  except TypeError:
    return _roll_dynamic(arr, asarray(shift), axis)
  else:
    return _roll_static(arr, shift, axis)
