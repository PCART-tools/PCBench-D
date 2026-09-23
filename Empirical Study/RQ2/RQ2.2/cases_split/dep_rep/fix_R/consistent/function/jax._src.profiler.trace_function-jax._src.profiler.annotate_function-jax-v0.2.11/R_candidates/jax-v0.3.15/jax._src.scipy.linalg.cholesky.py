@_wraps(scipy.linalg.cholesky,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
def cholesky(a, lower=False, overwrite_a=False, check_finite=True):
  del overwrite_a, check_finite
  return _cholesky(a, lower)
