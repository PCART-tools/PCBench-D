@util._wraps(np.apply_over_axes)
def apply_over_axes(func: Callable[[ArrayLike, int], Array], a: ArrayLike,
                    axes: Sequence[int]) -> Array:
  a_arr = asarray(a)
  for axis in axes:
    b = func(a_arr, axis)
    if b.ndim == a_arr.ndim:
      a_arr = b
    elif b.ndim == a_arr.ndim - 1:
      a_arr = expand_dims(b, axis)
    else:
      raise ValueError("function is not returning an array of the correct shape")
  return a_arr
