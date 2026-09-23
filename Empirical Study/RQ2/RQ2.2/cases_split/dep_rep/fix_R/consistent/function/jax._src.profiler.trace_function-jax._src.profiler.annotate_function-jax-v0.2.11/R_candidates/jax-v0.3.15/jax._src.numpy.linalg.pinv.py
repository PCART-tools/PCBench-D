@partial(custom_jvp, nondiff_argnums=(1,))
@_wraps(np.linalg.pinv, lax_description=textwrap.dedent("""\
    It differs only in default value of `rcond`. In `numpy.linalg.pinv`, the
    default `rcond` is `1e-15`. Here the default is
    `10. * max(num_rows, num_cols) * jnp.finfo(dtype).eps`.
    """))
@jit
def pinv(a, rcond=None):
  # Uses same algorithm as
  # https://github.com/numpy/numpy/blob/v1.17.0/numpy/linalg/linalg.py#L1890-L1979
  a = jnp.conj(a)
  if rcond is None:
    max_rows_cols = max(a.shape[-2:])
    rcond = 10. * max_rows_cols * jnp.array(jnp.finfo(a.dtype).eps)
  rcond = jnp.asarray(rcond)
  u, s, vh = svd(a, full_matrices=False)
  # Singular values less than or equal to ``rcond * largest_singular_value``
  # are set to zero.
  rcond = lax.expand_dims(rcond[..., jnp.newaxis], range(s.ndim - rcond.ndim - 1))
  cutoff = rcond * jnp.amax(s, axis=-1, keepdims=True, initial=-jnp.inf)
  s = jnp.where(s > cutoff, s, jnp.inf).astype(u.dtype)
  res = jnp.matmul(_T(vh), jnp.divide(_T(u), s[..., jnp.newaxis]))
  return lax.convert_element_type(res, a.dtype)
