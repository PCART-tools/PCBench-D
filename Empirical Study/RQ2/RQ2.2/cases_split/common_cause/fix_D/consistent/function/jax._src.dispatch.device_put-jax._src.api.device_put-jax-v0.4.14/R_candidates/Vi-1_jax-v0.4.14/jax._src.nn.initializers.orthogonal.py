@export
def orthogonal(scale: RealNumeric = 1.0,
               column_axis: int = -1,
               dtype: DTypeLikeInexact = jnp.float_) -> Initializer:
  """
  Builds an initializer that returns uniformly distributed orthogonal matrices.

  If the shape is not square, the matrices will have orthonormal rows or columns
  depending on which side is smaller.

  Args:
    scale: the upper bound of the uniform distribution.
    column_axis: the axis that contains the columns that should be orthogonal.
    dtype: the default dtype of the weights.

  Returns:
    An orthogonal initializer.

  Example:

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.orthogonal()
  >>> initializer(jax.random.PRNGKey(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 3.9026976e-01,  7.2495741e-01, -5.6756169e-01],
         [ 8.8047469e-01, -4.7409311e-01, -1.3157725e-04]],            dtype=float32)
  """
  def init(key: KeyArray,
           shape: core.Shape,
           dtype: DTypeLikeInexact = dtype) -> Array:
    dtype = dtypes.canonicalize_dtype(dtype)
    if len(shape) < 2:
      raise ValueError("orthogonal initializer requires at least a 2D shape")
    n_rows, n_cols = math.prod(shape) // shape[column_axis], shape[column_axis]
    matrix_shape = (n_cols, n_rows) if n_rows < n_cols else (n_rows, n_cols)
    A = random.normal(key, matrix_shape, dtype)
    Q, R = jnp.linalg.qr(A)
    diag_sign = lax.broadcast_to_rank(jnp.sign(jnp.diag(R)), rank=Q.ndim)
    Q *= diag_sign # needed for a uniform distribution
    if n_rows < n_cols: Q = Q.T
    Q = jnp.reshape(Q, tuple(np.delete(shape, column_axis)) + (shape[column_axis],))
    Q = jnp.moveaxis(Q, -1, column_axis)
    return scale * Q
  return init
