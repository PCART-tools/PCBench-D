@implements(getattr(np.linalg, "matrix_norm", None))
def matrix_norm(x: ArrayLike, /, *, keepdims: bool = False, ord: str = 'fro') -> Array:
  """
  Computes the matrix norm of a matrix (or a stack of matrices) x.
  """
  check_arraylike('jnp.linalg.matrix_norm', x)
  return norm(x, ord=ord, keepdims=keepdims, axis=(-2, -1))
