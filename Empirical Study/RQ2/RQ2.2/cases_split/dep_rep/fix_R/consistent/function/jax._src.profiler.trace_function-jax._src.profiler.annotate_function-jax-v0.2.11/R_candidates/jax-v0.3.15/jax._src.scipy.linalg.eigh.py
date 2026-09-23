@_wraps(scipy.linalg.eigh,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'overwrite_b', 'check_finite'))
def eigh(a, b=None, lower=True, eigvals_only=False, overwrite_a=False,
         overwrite_b=False, turbo=True, eigvals=None, type=1,
         check_finite=True):
  del overwrite_a, overwrite_b, turbo, check_finite
  return _eigh(a, b, lower, eigvals_only, eigvals, type)
