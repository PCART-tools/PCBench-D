@implements(scipy.linalg.qr,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'check_finite', 'lwork'))
def qr(a: ArrayLike, overwrite_a: bool = False, lwork: Any = None, mode: str = "full",
       pivoting: bool = False, check_finite: bool = True) -> tuple[Array] | tuple[Array, Array]:
  del overwrite_a, lwork, check_finite  # unused
  return _qr(a, mode, pivoting)
