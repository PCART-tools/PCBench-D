@_wraps(scipy.linalg.cho_factor,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite'))
def cho_factor(a: ArrayLike, lower: bool = False, overwrite_a: bool = False,
               check_finite: bool = True) -> tuple[Array, bool]:
  del overwrite_a, check_finite  # Unused
  return (cholesky(a, lower=lower), lower)
