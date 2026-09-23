@_wraps(scipy.linalg.cho_factor,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
def cho_factor(a, lower=False, overwrite_a=False, check_finite=True):
  return (cholesky(a, lower=lower), lower)
