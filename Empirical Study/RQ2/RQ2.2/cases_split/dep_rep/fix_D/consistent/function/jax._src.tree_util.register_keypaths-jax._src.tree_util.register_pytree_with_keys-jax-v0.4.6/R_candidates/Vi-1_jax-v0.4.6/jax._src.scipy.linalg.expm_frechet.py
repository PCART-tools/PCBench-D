@_wraps(scipy.linalg.expm_frechet, lax_description=_expm_frechet_description)
@partial(jit, static_argnames=('method', 'compute_expm'))
def expm_frechet(A: ArrayLike, E: ArrayLike, *, method: Optional[str] = None,
                 compute_expm: bool = True) -> Union[Array, Tuple[Array, Array]]:
  A = jnp.asarray(A)
  E = jnp.asarray(E)
  if A.ndim != 2 or A.shape[0] != A.shape[1]:
    raise ValueError('expected A to be a square matrix')
  if E.ndim != 2 or E.shape[0] != E.shape[1]:
    raise ValueError('expected E to be a square matrix')
  if A.shape != E.shape:
    raise ValueError('expected A and E to be the same shape')
  if method is None:
    method = 'SPS'
  if method == 'SPS':
    bound_fun = partial(expm, upper_triangular=False, max_squarings=16)
    expm_A, expm_frechet_AE = jvp(bound_fun, (A,), (E,))
  else:
    raise ValueError('only method=\'SPS\' is supported')
  if compute_expm:
    return expm_A, expm_frechet_AE
  else:
    return expm_frechet_AE
