@_wraps(scipy.linalg.lu_solve,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_b', 'check_finite'))
@partial(jit, static_argnames=('trans', 'overwrite_b', 'check_finite'))
def lu_solve(lu_and_piv, b, trans=0, overwrite_b=False, check_finite=True):
  del overwrite_b, check_finite
  lu, pivots = lu_and_piv
  m, n = lu.shape[-2:]
  perm = lax_linalg.lu_pivots_to_permutation(pivots, m)
  return lax_linalg.lu_solve(lu, perm, b, trans)
