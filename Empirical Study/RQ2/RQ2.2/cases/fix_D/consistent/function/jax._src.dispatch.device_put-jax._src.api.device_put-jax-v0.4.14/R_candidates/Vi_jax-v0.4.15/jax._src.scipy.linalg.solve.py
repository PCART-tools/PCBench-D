@_wraps(scipy.linalg.solve,
        lax_description=_no_overwrite_and_chkfinite_doc, skip_params=('overwrite_a', 'overwrite_b', 'debug', 'check_finite'))
def solve(a: ArrayLike, b: ArrayLike, sym_pos: bool = False, lower: bool = False,
          overwrite_a: bool = False, overwrite_b: bool = False, debug: bool = False,
          check_finite: bool = True, assume_a: str = 'gen') -> Array:
  # TODO(jakevdp) remove sym_pos argument after October 2022
  del overwrite_a, overwrite_b, debug, check_finite  #unused
  valid_assume_a = ['gen', 'sym', 'her', 'pos']
  if assume_a not in valid_assume_a:
    raise ValueError(f"Expected assume_a to be one of {valid_assume_a}; got {assume_a!r}")
  if sym_pos:
    warnings.warn("The sym_pos argument to solve() is deprecated and will be removed "
                  "in a future JAX release. Use assume_a='pos' instead.",
                  category=FutureWarning, stacklevel=2)
    assume_a = 'pos'
  return _solve(a, b, assume_a, lower)
