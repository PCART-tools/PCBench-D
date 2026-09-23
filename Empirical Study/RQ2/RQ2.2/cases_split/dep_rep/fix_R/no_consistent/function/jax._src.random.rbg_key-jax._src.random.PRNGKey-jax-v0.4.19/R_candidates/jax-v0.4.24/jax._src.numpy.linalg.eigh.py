@implements(np.linalg.eigh)
@partial(jit, static_argnames=('UPLO', 'symmetrize_input'))
def eigh(a: ArrayLike, UPLO: str | None = None,
         symmetrize_input: bool = True) -> EighResult:
  check_arraylike("jnp.linalg.eigh", a)
  if UPLO is None or UPLO == "L":
    lower = True
  elif UPLO == "U":
    lower = False
  else:
    msg = f"UPLO must be one of None, 'L', or 'U', got {UPLO}"
    raise ValueError(msg)

  a, = promote_dtypes_inexact(jnp.asarray(a))
  v, w = lax_linalg.eigh(a, lower=lower, symmetrize_input=symmetrize_input)
  return EighResult(w, v)
