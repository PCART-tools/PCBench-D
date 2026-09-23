@partial(custom_jvp, nondiff_argnums=(1, 2))
@implements(np.linalg.pinv, lax_description=textwrap.dedent("""\
    It differs only in default value of `rcond`. In `numpy.linalg.pinv`, the
    default `rcond` is `1e-15`. Here the default is
    `10. * max(num_rows, num_cols) * jnp.finfo(dtype).eps`.
    """))
@partial(jit, static_argnames=('hermitian',))
def pinv(a: ArrayLike, rcond: ArrayLike | None = None,
         hermitian: bool = False) -> Array:
  # Uses same algorithm as
  # https://github.com/numpy/numpy/blob/v1.17.0/numpy/linalg/linalg.py#L1890-L1979
  check_arraylike("jnp.linalg.pinv", a)
  arr = jnp.asarray(a)
  m, n = arr.shape[-2:]
  if m == 0 or n == 0:
    return jnp.empty(arr.shape[:-2] + (n, m), arr.dtype)
  arr = ufuncs.conj(arr)
  if rcond is None:
    max_rows_cols = max(arr.shape[-2:])
    rcond = 10. * max_rows_cols * jnp.array(jnp.finfo(arr.dtype).eps)
  rcond = jnp.asarray(rcond)
  u, s, vh = svd(arr, full_matrices=False, hermitian=hermitian)
  # Singular values less than or equal to ``rcond * largest_singular_value``
  # are set to zero.
  rcond = lax.expand_dims(rcond[..., jnp.newaxis], range(s.ndim - rcond.ndim - 1))
  cutoff = rcond * s[..., 0:1]
  s = jnp.where(s > cutoff, s, jnp.inf).astype(u.dtype)
  res = jnp.matmul(vh.mT, ufuncs.divide(u.mT, s[..., jnp.newaxis]),
                   precision=lax.Precision.HIGHEST)
  return lax.convert_element_type(res, arr.dtype)
