@implements(np.linalg.eigvalsh)
@partial(jit, static_argnames=('UPLO',))
def eigvalsh(a: ArrayLike, UPLO: str | None = 'L') -> Array:
  check_arraylike("jnp.linalg.eigvalsh", a)
  w, _ = eigh(a, UPLO)
  return w
