@_wraps(scipy.linalg.schur)
def schur(a: ArrayLike, output: str = 'real') -> Tuple[Array, Array]:
  if output not in ('real', 'complex'):
    raise ValueError(
      f"Expected 'output' to be either 'real' or 'complex', got {output=}.")
  return _schur(a, output)
