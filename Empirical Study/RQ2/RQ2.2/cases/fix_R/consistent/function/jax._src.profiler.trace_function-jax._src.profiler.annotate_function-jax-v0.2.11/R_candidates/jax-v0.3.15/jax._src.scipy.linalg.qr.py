@_wraps(scipy.linalg.qr,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
def qr(a, overwrite_a=False, lwork=None, mode="full", pivoting=False,
       check_finite=True):
  del overwrite_a, lwork, check_finite
  return _qr(a, mode, pivoting)
