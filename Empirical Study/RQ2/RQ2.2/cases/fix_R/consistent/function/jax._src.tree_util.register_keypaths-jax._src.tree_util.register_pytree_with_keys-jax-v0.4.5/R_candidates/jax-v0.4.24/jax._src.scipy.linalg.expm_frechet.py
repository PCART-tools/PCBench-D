@implements(scipy.linalg.expm_frechet, lax_description=_expm_frechet_description)
@partial(jit, static_argnames=('method', 'compute_expm'))
def expm_frechet(A: ArrayLike, E: ArrayLike, *, method: str | None = None,
                 compute_expm: bool = True) -> Array | tuple[Array, Array]:
  A_arr = jnp.asarray(A)
  E_arr = jnp.asarray(E)
  if A_arr.ndim != 2 or A_arr.shape[0] != A_arr.shape[1]:
    raise ValueError('expected A to be a square matrix')
  if E_arr.ndim != 2 or E_arr.shape[0] != E_arr.shape[1]:
    raise ValueError('expected E to be a square matrix')
  if A_arr.shape != E_arr.shape:
    raise ValueError('expected A and E to be the same shape')
  if method is None:
    method = 'SPS'
  if method == 'SPS':
    bound_fun = partial(expm, upper_triangular=False, max_squarings=16)
    expm_A, expm_frechet_AE = jvp(bound_fun, (A_arr,), (E_arr,))
  else:
    raise ValueError('only method=\'SPS\' is supported')
  if compute_expm:
    return expm_A, expm_frechet_AE
  else:
    return expm_frechet_AE
