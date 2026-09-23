@_wraps(scipy.linalg.eigh,
        lax_description=_no_overwrite_and_chkfinite_doc,
        skip_params=('overwrite_a', 'overwrite_b', 'turbo', 'check_finite'))
def eigh(a: ArrayLike, b: Optional[ArrayLike] = None, lower: bool = True,
         eigvals_only: bool = False, overwrite_a: bool = False,
         overwrite_b: bool = False, turbo: bool = True, eigvals: None = None,
         type: int = 1, check_finite: bool = True) -> Union[Array, Tuple[Array, Array]]:
  del overwrite_a, overwrite_b, turbo, check_finite  # unused
  return _eigh(a, b, lower, eigvals_only, eigvals, type)
