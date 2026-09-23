@_wraps(scipy.linalg.schur)
def schur(a, output='real'):
  if output not in ('real', 'complex'):
    raise ValueError(
      f"Expected 'output' to be either 'real' or 'complex', got output={output}.")
  return _schur(a, output)
