@_wraps(scipy.linalg.hessenberg, lax_description=_no_overwrite_and_chkfinite_doc)
@partial(jit, static_argnames=('calc_q', 'check_finite', 'overwrite_a'))
def hessenberg(a: ArrayLike, *, calc_q: bool = False, overwrite_a: bool = False,
               check_finite: bool = True) -> Union[Array, tuple[Array, Array]]:
  del overwrite_a, check_finite
  n = jnp.shape(a)[-1]
  if n == 0:
    if calc_q:
      return jnp.zeros_like(a), jnp.zeros_like(a)
    else:
      return jnp.zeros_like(a)
  a_out, taus = lax_linalg.hessenberg(a)
  h = jnp.triu(a_out, -1)
  if calc_q:
    q = lax_linalg.householder_product(a_out[..., 1:, :-1], taus)
    batch_dims = a_out.shape[:-2]
    q = jnp.block([[jnp.ones(batch_dims + (1, 1), dtype=a_out.dtype),
                    jnp.zeros(batch_dims + (1, n - 1), dtype=a_out.dtype)],
                   [jnp.zeros(batch_dims + (n - 1, 1), dtype=a_out.dtype), q]])
    return h, q
  else:
    return h
