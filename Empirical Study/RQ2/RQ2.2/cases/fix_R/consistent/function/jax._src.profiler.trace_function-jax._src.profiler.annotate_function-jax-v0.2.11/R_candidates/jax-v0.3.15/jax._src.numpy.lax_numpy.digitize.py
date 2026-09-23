@_wraps(np.digitize)
@partial(jit, static_argnames=('right',))
def digitize(x, bins, right=False):
  _check_arraylike("digitize", x, bins)
  right = core.concrete_or_error(bool, right, "right argument of jnp.digitize()")
  if ndim(bins) != 1:
    raise ValueError(f"digitize: bins must be a 1-dimensional array; got bins={bins}")
  if len(bins) == 0:
    return zeros(x, dtype=dtypes.canonicalize_dtype(int_))
  side = 'right' if not right else 'left'
  return where(
    bins[-1] >= bins[0],
    searchsorted(bins, x, side=side),
    len(bins) - searchsorted(bins[::-1], x, side=side)
  )
