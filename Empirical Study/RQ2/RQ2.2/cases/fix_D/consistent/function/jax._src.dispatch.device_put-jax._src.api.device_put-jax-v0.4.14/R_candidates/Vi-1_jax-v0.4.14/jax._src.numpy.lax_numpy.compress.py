@util._wraps(np.compress, skip_params=['out'])
def compress(condition: ArrayLike, a: ArrayLike, axis: Optional[int] = None,
             out: None = None) -> Array:
  util.check_arraylike("compress", condition, a)
  condition_arr = asarray(condition).astype(bool)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.compress is not supported.")
  if condition_arr.ndim != 1:
    raise ValueError("condition must be a 1D array")
  if axis is None:
    axis = 0
    arr = ravel(a)
  else:
    arr = moveaxis(a, axis, 0)
  condition_arr, extra = condition_arr[:arr.shape[0]], condition_arr[arr.shape[0]:]
  if reductions.any(extra):
    raise ValueError("condition contains entries that are out of bounds")
  arr = arr[:condition_arr.shape[0]]
  return moveaxis(arr[condition_arr], 0, axis)
