@_wraps(scipy.linalg.solve_triangular,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_b', 'debug', 'check_finite'))
def solve_triangular(a, b, trans=0, lower=False, unit_diagonal=False,
                     overwrite_b=False, debug=None, check_finite=True):
  del overwrite_b, debug, check_finite
  return _solve_triangular(a, b, trans, lower, unit_diagonal)
