@_wraps(scipy.linalg.solve_triangular,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_b', 'debug', 'check_finite'))
def solve_triangular(a: ArrayLike, b: ArrayLike, trans: Union[int, str] = 0, lower: bool = False,
                     unit_diagonal: bool = False, overwrite_b: bool = False,
                     debug: Any = None, check_finite: bool = True) -> Array:
  del overwrite_b, debug, check_finite  # unused
  return _solve_triangular(a, b, trans, lower, unit_diagonal)
