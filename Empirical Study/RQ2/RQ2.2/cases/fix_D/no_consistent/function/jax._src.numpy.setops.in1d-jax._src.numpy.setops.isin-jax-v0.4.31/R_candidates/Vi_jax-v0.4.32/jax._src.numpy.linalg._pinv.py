@partial(custom_jvp, nondiff_argnums=(1, 2))
@partial(jit, static_argnames=('hermitian'))
def _pinv(a: ArrayLike, rtol: ArrayLike | None = None, hermitian: bool = False) -> Array:
  # Uses same algorithm as
  # https://github.com/numpy/numpy/blob/v1.17.0/numpy/linalg/linalg.py#L1890-L1979
  check_arraylike("jnp.linalg.pinv", a)
  arr, = promote_dtypes_inexact(jnp.asarray(a))
  m, n = arr.shape[-2:]
  if m == 0 or n == 0:
    return jnp.empty(arr.shape[:-2] + (n, m), arr.dtype)
  arr = ufuncs.conj(arr)
  if rtol is None:
    max_rows_cols = max(arr.shape[-2:])
    rtol = 10. * max_rows_cols * jnp.array(jnp.finfo(arr.dtype).eps)
  rtol = jnp.asarray(rtol)
  u, s, vh = svd(arr, full_matrices=False, hermitian=hermitian)
  # Singular values less than or equal to ``rtol * largest_singular_value``
  # are set to zero.
  rtol = lax.expand_dims(rtol[..., jnp.newaxis], range(s.ndim - rtol.ndim - 1))
  cutoff = rtol * s[..., 0:1]
  s = jnp.where(s > cutoff, s, jnp.inf).astype(u.dtype)
  res = jnp.matmul(vh.mT, ufuncs.divide(u.mT, s[..., jnp.newaxis]),
                   precision=lax.Precision.HIGHEST)
  return lax.convert_element_type(res, arr.dtype)
