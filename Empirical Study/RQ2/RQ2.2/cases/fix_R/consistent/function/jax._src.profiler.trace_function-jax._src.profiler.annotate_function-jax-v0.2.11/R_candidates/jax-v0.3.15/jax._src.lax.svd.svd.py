@functools.partial(jax.jit, static_argnums=(1, 2, 3, 4))
def svd(a: Any,
        full_matrices: bool,
        compute_uv: bool = True,
        hermitian: bool = False,
        max_iterations: int = 10) -> Union[Any, Sequence[Any]]:
  """Singular value decomposition.

  Args:
    a: A matrix of shape `m x n`.
    full_matrices: If True, `u` and `vh` have the shapes `m x m` and `n x n`,
      respectively. If False, the shapes are `m x k` and `k x n`, respectively,
      where `k = min(m, n)`.
    compute_uv: Whether to compute also `u` and `v` in addition to `s`.
    hermitian: True if `a` is Hermitian.
    max_iterations: The predefined maximum number of iterations of QDWH.

  Returns:
    A 3-tuple (`u`, `s`, `vh`), where `u` and `vh` are unitary matrices,
    `s` is vector of length `k` containing the singular values in the
    non-increasing order, and `k = min(m, n)`. The shapes of `u` and `vh`
    depend on the value of `full_matrices`. For `compute_uv=False`,
    only `s` is returned.
  """
  full_matrices = core.concrete_or_error(
      bool, full_matrices, 'The `full_matrices` argument must be statically '
      'specified to use `svd` within JAX transformations.')

  compute_uv = core.concrete_or_error(
      bool, compute_uv, 'The `compute_uv` argument must be statically '
      'specified to use `svd` within JAX transformations.')

  hermitian = core.concrete_or_error(
      bool, hermitian, 'The `hermitian` argument must be statically '
      'specified to use `qdwh` within JAX transformations.')

  max_iterations = core.concrete_or_error(
      int, max_iterations, 'The `max_iterations` argument must be statically '
      'specified to use `qdwh` within JAX transformations.')

  # QDWH algorithm fails at zero-matrix `A` and produces all NaNs, which can
  # be seen from a dynamically weighted Halley (DWH) iteration:
  # X_{k+1} = X_k(a_k I + b_k {X_k}^H X_k)(I + c_k {X_k}^H X_k)^{−1} and
  # X_0 = A/alpha, where alpha = ||A||_2, the triplet (a_k, b_k, c_k) are
  # weighting parameters, and X_k denotes the k^{th} iterate.
  return jax.lax.cond(jnp.all(a == 0),
                      functools.partial(_zero_svd, full_matrices=full_matrices,
                                        compute_uv=compute_uv),
                      functools.partial(_qdwh_svd, full_matrices=full_matrices,
                                        compute_uv=compute_uv,
                                        hermitian=hermitian,
                                        max_iterations=max_iterations),
                      operand=(a))
