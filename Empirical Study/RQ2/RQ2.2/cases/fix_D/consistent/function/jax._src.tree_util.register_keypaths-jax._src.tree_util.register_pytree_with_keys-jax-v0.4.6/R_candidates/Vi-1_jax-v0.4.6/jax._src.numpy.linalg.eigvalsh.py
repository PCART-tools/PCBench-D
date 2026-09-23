@_wraps(np.linalg.eigvalsh)
@partial(jit, static_argnames=('UPLO',))
def eigvalsh(a: ArrayLike, UPLO: Optional[str] = 'L') -> Array:
  _check_arraylike("jnp.linalg.eigvalsh", a)
  w, _ = eigh(a, UPLO)
  return w
