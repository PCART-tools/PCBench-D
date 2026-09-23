@partial(jit, static_argnames=('mode', 'pivoting'))
def _qr(a, mode, pivoting):
  if pivoting:
    raise NotImplementedError(
        "The pivoting=True case of qr is not implemented.")
  if mode in ("full", "r"):
    full_matrices = True
  elif mode == "economic":
    full_matrices = False
  else:
    raise ValueError(f"Unsupported QR decomposition mode '{mode}'")
  a, = _promote_dtypes_inexact(jnp.asarray(a))
  q, r = lax_linalg.qr(a, full_matrices=full_matrices)
  if mode == "r":
    return (r,)
  return q, r
