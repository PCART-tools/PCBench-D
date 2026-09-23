@_wraps(np.apply_over_axes)
def apply_over_axes(func, a, axes):
  for axis in axes:
    b = func(a, axis=axis)
    if b.ndim == a.ndim:
      a = b
    elif b.ndim == a.ndim - 1:
      a = expand_dims(b, axis)
    else:
      raise ValueError("function is not returning an array of the correct shape")
  return a
