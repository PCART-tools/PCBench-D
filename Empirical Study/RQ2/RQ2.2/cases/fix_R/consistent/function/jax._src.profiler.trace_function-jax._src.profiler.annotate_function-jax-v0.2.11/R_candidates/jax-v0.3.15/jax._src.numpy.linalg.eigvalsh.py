@_wraps(np.linalg.eigvalsh)
@partial(jit, static_argnames=('UPLO',))
def eigvalsh(a, UPLO='L'):
  w, _ = eigh(a, UPLO)
  return w
