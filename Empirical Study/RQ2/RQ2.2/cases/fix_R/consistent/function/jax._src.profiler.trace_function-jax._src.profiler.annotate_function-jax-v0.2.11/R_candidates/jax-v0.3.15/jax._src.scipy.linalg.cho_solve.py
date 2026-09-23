@_wraps(scipy.linalg.cho_solve, update_doc=False,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_b', 'check_finite'))
def cho_solve(c_and_lower, b, overwrite_b=False, check_finite=True):
  del overwrite_b, check_finite
  c, lower = c_and_lower
  return _cho_solve(c, b, lower)
