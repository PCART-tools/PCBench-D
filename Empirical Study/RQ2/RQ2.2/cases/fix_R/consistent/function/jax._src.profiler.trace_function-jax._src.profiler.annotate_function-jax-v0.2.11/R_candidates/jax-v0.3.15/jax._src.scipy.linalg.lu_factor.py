@_wraps(scipy.linalg.lu_factor,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
@partial(jit, static_argnames=('overwrite_a', 'check_finite'))
def lu_factor(a, overwrite_a=False, check_finite=True):
  del overwrite_a, check_finite
  a, = _promote_dtypes_inexact(jnp.asarray(a))
  lu, pivots, _ = lax_linalg.lu(a)
  return lu, pivots
