@functools.partial(jax.jit, static_argnames=('is_hermitian',))
def qdwh(x, *, is_hermitian=False, max_iterations=None, eps=None,
         dynamic_shape: Optional[Tuple[int, int]] = None):
  """QR-based dynamically weighted Halley iteration for polar decomposition.

  Args:
    x: A full-rank matrix, with shape `M x N`. The matrix may be
      padded up to that size from a smaller true shape (``dynamic_shape``).
    is_hermitian: True if `x` is Hermitian. Default to `False`.
    eps: The final result will satisfy
      ``|x_k - x_k-1| < |x_k| * (4*eps)**(1/3)`` where `x_k` is the iterate.
    max_iterations: Iterations will terminate after this many steps even if the
      above is unsatisfied.
    dynamic_shape: the unpadded shape as an ``(m, n)`` tuple; optional.

  Returns:
    A four-tuple of (u, h, num_iters, is_converged) containing the
    polar decomposition of `x = u * h`, the number of iterations to compute `u`,
    and `is_converged`, whose value is `True` when the convergence is achieved
    within the maximum number of iterations.
  """
  is_hermitian = core.concrete_or_error(
      bool, is_hermitian, 'The `is_hermitian` argument must be statically '
      'specified to use `qdwh` within JAX transformations.')

  if max_iterations is None:
    max_iterations = 10

  M, N = x.shape
  if M < N:
    raise ValueError('The input matrix of shape M x N must have M >= N.')
  if dynamic_shape is not None:
    m, n = dynamic_shape
    x = _mask(x, (m, n))
  else:
    m, n = M, N

  with jax.default_matmul_precision('float32'):
    u, h, num_iters, is_converged = _qdwh(x, m, n, is_hermitian, max_iterations,
                                          eps)


  return u, h, num_iters, is_converged
