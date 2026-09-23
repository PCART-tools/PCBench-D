@_wraps(np.linalg.qr)
@partial(jit, static_argnames=('mode',))
def qr(a: ArrayLike, mode: str = "reduced") -> Union[Array, tuple[Array, Array]]:
  check_arraylike("jnp.linalg.qr", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  if mode == "raw":
    a, taus = lax_linalg.geqrf(a)
    return a.mT, taus
  if mode in ("reduced", "r", "full"):
    full_matrices = False
  elif mode == "complete":
    full_matrices = True
  else:
    raise ValueError(f"Unsupported QR decomposition mode '{mode}'")
  q, r = lax_linalg.qr(a, full_matrices=full_matrices)
  if mode == "r":
    return r
  return q, r
