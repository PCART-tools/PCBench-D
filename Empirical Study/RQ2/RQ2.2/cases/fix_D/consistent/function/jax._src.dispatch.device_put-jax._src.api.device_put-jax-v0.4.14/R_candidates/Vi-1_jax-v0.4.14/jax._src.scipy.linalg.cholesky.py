@_wraps(scipy.linalg.cholesky,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
def cholesky(a: ArrayLike, lower: bool = False, overwrite_a: bool = False,
             check_finite: bool = True) -> Array:
  del overwrite_a, check_finite  # Unused
  return _cholesky(a, lower)
