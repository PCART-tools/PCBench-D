@implements(scipy.linalg.solve,
        lax_description=_no_overwrite_and_chkfinite_doc,
        skip_params=('overwrite_a', 'overwrite_b', 'debug', 'check_finite'))
def solve(a: ArrayLike, b: ArrayLike, lower: bool = False,
          overwrite_a: bool = False, overwrite_b: bool = False, debug: bool = False,
          check_finite: bool = True, assume_a: str = 'gen') -> Array:
  del overwrite_a, overwrite_b, debug, check_finite  #unused
  valid_assume_a = ['gen', 'sym', 'her', 'pos']
  if assume_a not in valid_assume_a:
    raise ValueError(f"Expected assume_a to be one of {valid_assume_a}; got {assume_a!r}")
  return _solve(a, b, assume_a, lower)
