@_wraps(osp_signal.detrend)
def detrend(data, axis=-1, type='linear', bp=0, overwrite_data=None):
  if overwrite_data is not None:
    raise NotImplementedError("overwrite_data argument not implemented.")
  if type not in ['constant', 'linear']:
    raise ValueError("Trend type must be 'linear' or 'constant'.")
  data, = _promote_dtypes_inexact(jnp.asarray(data))
  if type == 'constant':
    return data - data.mean(axis, keepdims=True)
  else:
    N = data.shape[axis]
    # bp is static, so we use np operations to avoid pushing to device.
    bp = np.sort(np.unique(np.r_[0, bp, N]))
    if bp[0] < 0 or bp[-1] > N:
      raise ValueError("Breakpoints must be non-negative and less than length of data along given axis.")
    data = jnp.moveaxis(data, axis, 0)
    shape = data.shape
    data = data.reshape(N, -1)
    for m in range(len(bp) - 1):
      Npts = bp[m + 1] - bp[m]
      A = jnp.vstack([
        jnp.ones(Npts, dtype=data.dtype),
        jnp.arange(1, Npts + 1, dtype=data.dtype) / Npts.astype(data.dtype)
      ]).T
      sl = slice(bp[m], bp[m + 1])
      coef, *_ = linalg.lstsq(A, data[sl])
      data = data.at[sl].add(-jnp.matmul(A, coef, precision=lax.Precision.HIGHEST))
    return jnp.moveaxis(data.reshape(shape), 0, axis)
