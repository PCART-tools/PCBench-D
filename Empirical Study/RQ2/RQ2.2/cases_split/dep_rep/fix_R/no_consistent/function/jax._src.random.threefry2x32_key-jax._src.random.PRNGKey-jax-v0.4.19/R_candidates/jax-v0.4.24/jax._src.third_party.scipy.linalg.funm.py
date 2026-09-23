@implements(scipy.linalg.funm, lax_description=_FUNM_LAX_DESCRIPTION)
def funm(A: ArrayLike, func: Callable[[Array], Array],
         disp: bool = True) -> Array | tuple[Array, Array]:
  A_arr = jnp.asarray(A)
  if A_arr.ndim != 2 or A_arr.shape[0] != A_arr.shape[1]:
    raise ValueError('expected square array_like input')

  T, Z = schur(A_arr)
  T, Z = rsf2csf(T, Z)

  F = jnp.diag(func(jnp.diag(T)))
  F = F.astype(T.dtype.char)

  F, minden = _algorithm_11_1_1(F, T)
  F = Z @ F @ Z.conj().T

  if disp:
    return F

  if F.dtype.char.lower() == 'e':
    tol = jnp.finfo(jnp.float16).eps
  if F.dtype.char.lower() == 'f':
    tol = jnp.finfo(jnp.float32).eps
  else:
    tol = jnp.finfo(jnp.float64).eps

  minden = jnp.where(minden == 0.0, tol, minden)
  err = jnp.where(jnp.any(jnp.isinf(F)), jnp.inf, jnp.minimum(1, jnp.maximum(
          tol, (tol / minden) * norm(jnp.triu(T, 1), 1))))

  return F, err
