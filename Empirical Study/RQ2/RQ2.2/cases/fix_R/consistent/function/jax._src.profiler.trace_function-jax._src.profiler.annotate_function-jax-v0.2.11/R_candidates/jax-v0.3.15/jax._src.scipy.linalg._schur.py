@partial(jit, static_argnames=('output',))
def _schur(a, output):
  if output == "complex":
    a = a.astype(dtypes._to_complex_dtype(a.dtype))
  return lax_linalg.schur(a)
