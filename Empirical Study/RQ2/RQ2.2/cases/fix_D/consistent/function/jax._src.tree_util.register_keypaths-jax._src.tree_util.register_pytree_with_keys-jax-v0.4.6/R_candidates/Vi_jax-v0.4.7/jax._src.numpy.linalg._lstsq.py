def _lstsq(a: ArrayLike, b: ArrayLike, rcond: Optional[float], *,
           numpy_resid: bool = False) -> Tuple[Array, Array, Array, Array]:
  # TODO: add lstsq to lax_linalg and implement this function via those wrappers.
  # TODO: add custom jvp rule for more robust lstsq differentiation
  a, b = promote_dtypes_inexact(a, b)
  if a.shape[0] != b.shape[0]:
    raise ValueError("Leading dimensions of input arrays must match")
  b_orig_ndim = b.ndim
  if b_orig_ndim == 1:
    b = b[:, None]
  if a.ndim != 2:
    raise TypeError(
      f"{a.ndim}-dimensional array given. Array must be two-dimensional")
  if b.ndim != 2:
    raise TypeError(
      f"{b.ndim}-dimensional array given. Array must be one or two-dimensional")
  m, n = a.shape
  dtype = a.dtype
  if a.size == 0:
    s = jnp.empty(0, dtype=a.dtype)
    rank = jnp.array(0, dtype=int)
    x = jnp.empty((n, *b.shape[1:]), dtype=a.dtype)
  else:
    if rcond is None:
      rcond = jnp.finfo(dtype).eps * max(n, m)
    else:
      rcond = jnp.where(rcond < 0, jnp.finfo(dtype).eps, rcond)
    u, s, vt = svd(a, full_matrices=False)
    mask = s >= jnp.array(rcond, dtype=s.dtype) * s[0]
    rank = mask.sum()
    safe_s = jnp.where(mask, s, 1).astype(a.dtype)
    s_inv = jnp.where(mask, 1 / safe_s, 0)[:, jnp.newaxis]
    uTb = jnp.matmul(u.conj().T, b, precision=lax.Precision.HIGHEST)
    x = jnp.matmul(vt.conj().T, s_inv * uTb, precision=lax.Precision.HIGHEST)
  # Numpy returns empty residuals in some cases. To allow compilation, we
  # default to returning full residuals in all cases.
  if numpy_resid and (rank < n or m <= n):
    resid = jnp.asarray([])
  else:
    b_estimate = jnp.matmul(a, x, precision=lax.Precision.HIGHEST)
    resid = norm(b - b_estimate, axis=0) ** 2
  if b_orig_ndim == 1:
    x = x.ravel()
  return x, resid, rank, s
