@_wraps(scipy.linalg.det,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
def det(a, overwrite_a=False, check_finite=True):
  del overwrite_a, check_finite
  return np_linalg.det(a)
