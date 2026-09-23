@util._wraps(np.digitize)
@partial(jit, static_argnames=('right',))
def digitize(x: ArrayLike, bins: ArrayLike, right: bool = False) -> Array:
  util._check_arraylike("digitize", x, bins)
  right = core.concrete_or_error(bool, right, "right argument of jnp.digitize()")
  bins_arr = asarray(bins)
  if bins_arr.ndim != 1:
    raise ValueError(f"digitize: bins must be a 1-dimensional array; got {bins=}")
  if bins_arr.shape[0] == 0:
    return zeros(x, dtype=dtypes.canonicalize_dtype(int_))
  side = 'right' if not right else 'left'
  return where(
    bins_arr[-1] >= bins_arr[0],
    searchsorted(bins_arr, x, side=side),
    len(bins_arr) - searchsorted(bins_arr[::-1], x, side=side)
  )
