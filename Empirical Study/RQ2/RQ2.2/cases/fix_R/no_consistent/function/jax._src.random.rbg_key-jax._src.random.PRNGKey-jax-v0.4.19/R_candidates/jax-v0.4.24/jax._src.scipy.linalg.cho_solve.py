@implements(scipy.linalg.cho_solve, update_doc=False,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_b', 'check_finite'))
def cho_solve(c_and_lower: tuple[ArrayLike, bool], b: ArrayLike,
              overwrite_b: bool = False, check_finite: bool = True) -> Array:
  del overwrite_b, check_finite  # Unused
  c, lower = c_and_lower
  return _cho_solve(c, b, lower)
