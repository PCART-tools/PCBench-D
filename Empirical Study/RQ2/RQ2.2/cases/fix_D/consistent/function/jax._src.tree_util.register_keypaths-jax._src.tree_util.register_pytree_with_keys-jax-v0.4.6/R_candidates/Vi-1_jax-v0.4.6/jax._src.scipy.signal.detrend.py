@_wraps(osp_signal.detrend)
def detrend(data: ArrayLike, axis: int = -1, type: str = 'linear', bp: int = 0,
            overwrite_data: None = None) -> Array:
  if overwrite_data is not None:
    raise NotImplementedError("overwrite_data argument not implemented.")
  if type not in ['constant', 'linear']:
    raise ValueError("Trend type must be 'linear' or 'constant'.")
  data_arr, = _promote_dtypes_inexact(jnp.asarray(data))
  if type == 'constant':
    return data_arr - data_arr.mean(axis, keepdims=True)
  else:
    N = data_arr.shape[axis]
    # bp is static, so we use np operations to avoid pushing to device.
    bp_arr = np.sort(np.unique(np.r_[0, bp, N]))
    if bp_arr[0] < 0 or bp_arr[-1] > N:
      raise ValueError("Breakpoints must be non-negative and less than length of data along given axis.")
    data_arr = jnp.moveaxis(data_arr, axis, 0)
    shape = data_arr.shape
    data_arr = data_arr.reshape(N, -1)
    for m in range(len(bp_arr) - 1):
      Npts = bp_arr[m + 1] - bp_arr[m]
      A = jnp.vstack([
        jnp.ones(Npts, dtype=data_arr.dtype),
        jnp.arange(1, Npts + 1, dtype=data_arr.dtype) / Npts.astype(data_arr.dtype)
      ]).T
      sl = slice(bp_arr[m], bp_arr[m + 1])
      coef, *_ = linalg.lstsq(A, data_arr[sl])
      data_arr = data_arr.at[sl].add(-jnp.matmul(A, coef, precision=lax.Precision.HIGHEST))
    return jnp.moveaxis(data_arr.reshape(shape), 0, axis)
